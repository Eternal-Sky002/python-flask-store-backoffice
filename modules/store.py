from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import api_call

store_bp = Blueprint('store', __name__)

@store_bp.route('/stores')
def stores():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('GET', '/stores', headers=headers)
    stores = response.json() if response else []
    
    # Get all items to count per store
    items_response = api_call('GET', '/items', headers=headers)
    items = items_response.json() if items_response else []
    
    # Count items per store
    for store in stores:
        store_id = store.get('id')
        store['item_count'] = sum(1 for item in items if (item.get('store') and item['store'].get('id') == store_id) or (item.get('store_id') == store_id))
    
    return render_template('store/stores.html', stores=stores)

@store_bp.route('/stores/create', methods=['GET', 'POST'])
def create_store():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        headers = {'Authorization': f'Bearer {session.get("access_token")}'}
        
        store_data = {
            'name': request.form['name']
        }
        
        response = api_call('POST', '/stores', store_data, headers)
        
        if response and response.status_code == 201:
            flash('Store berhasil dibuat!', 'success')
            return redirect(url_for('store.stores'))
        else:
            flash('Gagal membuat store!', 'error')
    
    return render_template('store/create_store.html')

@store_bp.route('/stores/<int:store_id>/edit', methods=['GET', 'POST'])
def edit_store(store_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    if request.method == 'POST':
        store_data = {
            'name': request.form['name']
        }
        
        response = api_call('PUT', f'/stores/{store_id}', store_data, headers)
        
        if response and response.status_code == 200:
            flash('Store berhasil diupdate!', 'success')
            return redirect(url_for('store.stores'))
        else:
            flash('Gagal mengupdate store!', 'error')
    
    store_response = api_call('GET', f'/stores/{store_id}', headers=headers)
    store = store_response.json() if store_response else {}
    
    return render_template('store/edit_store.html', store=store)

@store_bp.route('/stores/<int:store_id>/delete', methods=['POST'])
def delete_store(store_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('DELETE', f'/stores/{store_id}', headers=headers)
    
    if response and response.status_code == 200:
        flash('Store berhasil dihapus!', 'success')
    else:
        flash('Gagal menghapus store!', 'error')
    
    return redirect(url_for('store.stores'))