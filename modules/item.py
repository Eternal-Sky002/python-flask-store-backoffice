from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import api_call

item_bp = Blueprint('item', __name__)

@item_bp.route('/items')
def items():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('GET', '/items', headers=headers)
    items = response.json() if response else []
    
    # Process items to extract store names from nested store object
    for item in items:
        if item.get('store') and isinstance(item['store'], dict):
            item['store_name'] = item['store'].get('name', 'Unknown Store')
        else:
            item['store_name'] = 'No Store'
    
    return render_template('item/item.html', items=items)

@item_bp.route('/items/create', methods=['GET', 'POST'])
def create_item():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    stores_response = api_call('GET', '/stores', headers=headers)
    stores = stores_response.json() if stores_response else []
    
    if request.method == 'POST':
        # First, create the item without tags
        item_data = {
            'name': request.form['name'],
            'price': float(request.form['price']),
            'store_id': int(request.form['store_id']),
            'qty': request.form['qty']
        }
        
        response = api_call('POST', '/items', item_data, headers)
        
        if response and response.status_code == 201:
            # Get the created item ID
            created_item = response.json()
            item_id = created_item.get('id')
            
            # Add tags separately
            selected_tag_ids = request.form.getlist('tag_ids')
            success_count = 0
            
            for tag_id in selected_tag_ids:
                tag_response = api_call('POST', f'/items/{item_id}/tag/{tag_id}', headers=headers)
                if tag_response and tag_response.status_code in [200, 201]:
                    success_count += 1
            
            if success_count > 0:
                flash(f'Item berhasil dibuat dengan {success_count} tag!', 'success')
            else:
                flash('Item berhasil dibuat!', 'success')
            
            return redirect(url_for('item.items'))
        else:
            flash('Gagal membuat item!', 'error')
    
    return render_template('item/create_item.html', stores=stores)

@item_bp.route('/api/stores/<int:store_id>/tags')
def get_store_tags(store_id):
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    tags_response = api_call('GET', f'/stores/{store_id}/tag', headers=headers)
    
    if tags_response:
        tags = tags_response.json()
        return {'tags': tags}
    else:
        return {'tags': []}

@item_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    if request.method == 'POST':
        # First, update the item without tags
        item_data = {
            'name': request.form['name'],
            'price': float(request.form['price']),
            'store_id': int(request.form['store_id'])
        }
        
        response = api_call('PUT', f'/items/{item_id}', item_data, headers)
        
        if response and response.status_code == 200:
            # Handle tag associations separately
            selected_tag_ids = request.form.getlist('tag_ids')
            
            # Get current item tags to compare
            item_response = api_call('GET', f'/items/{item_id}', headers=headers)
            current_tags = []
            if item_response:
                current_item = item_response.json()
                current_tags = [tag['id'] for tag in current_item.get('tags', [])]
            
            # Remove tags that are no longer selected
            for tag_id in current_tags:
                if str(tag_id) not in selected_tag_ids:
                    api_call('DELETE', f'/items/{item_id}/tag/{tag_id}', headers=headers)
            
            # Add new tags
            success_count = 0
            for tag_id in selected_tag_ids:
                if int(tag_id) not in current_tags:
                    tag_response = api_call('POST', f'/items/{item_id}/tag/{tag_id}', headers=headers)
                    if tag_response and tag_response.status_code in [200, 201]:
                        success_count += 1
            
            flash('Item berhasil diupdate!', 'success')
            return redirect(url_for('item.items'))
        else:
            flash('Gagal mengupdate item!', 'error')
    
    # Get item details and stores
    item_response = api_call('GET', f'/items/{item_id}', headers=headers)
    stores_response = api_call('GET', '/stores', headers=headers)
    
    item = item_response.json() if item_response else {}
    stores = stores_response.json() if stores_response else []
    
    return render_template('item/edit_item.html', item=item, stores=stores)

@item_bp.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('DELETE', f'/items/{item_id}', headers=headers)
    
    if response and response.status_code == 200:
        flash('Item berhasil dihapus!', 'success')
    else:
        flash('Gagal menghapus item!', 'error')
    
    return redirect(url_for('item.items'))

@item_bp.route('/items/<int:item_id>/tag/<int:tag_id>/remove', methods=['POST'])
def remove_item_tag(item_id, tag_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('DELETE', f'/items/{item_id}/tag/{tag_id}', headers=headers)
    
    if response and response.status_code == 200:
        flash('Tag berhasil dihapus dari item!', 'success')
    else:
        flash('Gagal menghapus tag dari item!', 'error')
    
    return redirect(url_for('item.edit_item', item_id=item_id))