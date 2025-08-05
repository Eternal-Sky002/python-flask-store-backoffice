from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import api_call
import base64
import json

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags')
def tags():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    # Get all stores
    stores_response = api_call('GET', '/stores', headers=headers)
    if stores_response and stores_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    
    stores = stores_response.json() if stores_response else []
    
    # Get tags for each store
    stores_with_tags = []
    for store in stores:
        store_tags_response = api_call('GET', f'/stores/{store["id"]}/tag', headers=headers)
        store_tags = store_tags_response.json() if store_tags_response else []
        
        # Encode tags as base64 to avoid template escaping issues
        tags_json = json.dumps(store_tags)
        tags_base64 = base64.b64encode(tags_json.encode('utf-8')).decode('utf-8')
        
        stores_with_tags.append({
            'store': store,
            'tags': store_tags,
            'tags_base64': tags_base64
        })
    
    return render_template('tag/tags.html', stores_with_tags=stores_with_tags)

@tag_bp.route('/tags/create', methods=['GET', 'POST'])
def create_tag():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}' }
    stores_response = api_call('GET', '/stores', headers=headers)
    
    if stores_response and stores_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    
    stores = stores_response.json() if stores_response else []
    
    if request.method == 'POST':
        store_id = request.form['store_id']
        tag_name = request.form['name']
        tag_data = {
            'name': tag_name
        }
        response = api_call('POST', f'/stores/{store_id}/tag', tag_data, headers)
        if response and response.status_code == 201:
            flash('Tag berhasil dibuat!', 'success')
            return redirect(url_for('tag.tags'))
        else:
            flash('Gagal membuat tag!', 'error')
    
    return render_template('tag/create_tag.html', stores=stores)

@tag_bp.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    if request.method == 'POST':
        tag_data = {
            'name': request.form['name']
        }
        
        response = api_call('PUT', f'/tags/{tag_id}', tag_data, headers)
        
        if response and response.status_code == 200:
            flash('Tag berhasil diupdate!', 'success')
            return redirect(url_for('tag.tags'))
        else:
            flash('Gagal mengupdate tag!', 'error')
    
    tag_response = api_call('GET', f'/tags/{tag_id}', headers=headers)
    tag = tag_response.json() if tag_response else {}
    
    return render_template('tag/edit_tag.html', tag=tag)

@tag_bp.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('DELETE', f'/tags/{tag_id}', headers=headers)
    
    if response and response.status_code == 200:
        flash('Tag berhasil dihapus!', 'success')
    else:
        flash('Gagal menghapus tag!', 'error')
    
    return redirect(url_for('tag.tags'))