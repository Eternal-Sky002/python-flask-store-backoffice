from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from config import api_call, api_wilayah_call

store_bp = Blueprint('store', __name__)

# untuk mengambil data kabupaten/kota
@store_bp.route('/stores/get_regencies/<provinsi_code>')
def get_regencies(provinsi_code):
    kabupaten_kota_response = api_wilayah_call('GET', f'/regencies/{provinsi_code}.json')
    kabupaten_kotas = kabupaten_kota_response.json().get('data', []) if kabupaten_kota_response else []
    # print(jsonify(kabupaten_kotas))
    return jsonify(kabupaten_kotas)

# untuk mengambil data kecamatan
@store_bp.route('/stores/get_districts/<kabupaten_kota_code>')
def get_districts(kabupaten_kota_code):
    kecamatan_response = api_wilayah_call('GET', f'/districts/{kabupaten_kota_code}.json')
    kecamatans = kecamatan_response.json().get('data', []) if kecamatan_response else []
    # print(jsonify(kecamatans))
    return jsonify(kecamatans)

# untuk mengambil data kelurahan
@store_bp.route('/stores/get_villages/<kecamatan_code>')
def get_villages(kecamatan_code):
    kelurahan_response = api_wilayah_call('GET', f'/villages/{kecamatan_code}.json')
    kelurahans = kelurahan_response.json().get('data', []) if kelurahan_response else []
    # print(jsonify(kelurahans))
    return jsonify(kelurahans)

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
    
    provinsi_response = api_wilayah_call('GET', '/provinces.json')
    provinsis = provinsi_response.json().get('data', []) if provinsi_response else []

    # print("Provinsis:", provinsi_response)
    
    if request.method == 'POST':
        headers = {'Authorization': f'Bearer {session.get("access_token")}'}
       
        provinsi_code = request.form['provinsi_code']
        kabupaten_kota_code = request.form['kabupaten_kota_code']
        kecamatan_code = request.form['kecamatan_code']
        kelurahan_code = request.form['kelurahan_code']

        # ambil nama provinsi dari provinsis yang sudah di-load
        provinsi_name = next((provinsi['name'] for provinsi in provinsis if provinsi['code'] == provinsi_code), None)

        # ambil kabupaten via API
        kabupaten_kota_response = api_wilayah_call('GET', f'/regencies/{provinsi_code}.json')
        kabupaten_kotas = kabupaten_kota_response.json().get('data', []) if kabupaten_kota_response else []
        kabupaten_kota_name = next((kabupaten_kota['name'] for kabupaten_kota in kabupaten_kotas if kabupaten_kota['code'] == kabupaten_kota_code), None)

        # ambil kecamatan via API
        kecamatan_response = api_wilayah_call('GET', f'/districts/{kabupaten_kota_code}.json')
        kecamatans = kecamatan_response.json().get('data', []) if kecamatan_response else []
        kecamatan_name = next((kecamatan['name'] for kecamatan in kecamatans if kecamatan['code'] == kecamatan_code), None)

        # ambil kelurahan via API
        kelurahan_response = api_wilayah_call('GET', f'/villages/{kecamatan_code}.json')
        kelurahans = kelurahan_response.json().get('data', []) if kelurahan_response else []
        kelurahan_name = next((kelurahan['name'] for kelurahan in kelurahans if kelurahan['code'] == kelurahan_code), None)
        
        store_data = {
            'name': request.form['name'],
            'provinsi': provinsi_name,
            'kabupaten_kota': kabupaten_kota_name,
            'kecamatan': kecamatan_name,
            'kelurahan': kelurahan_name
        }
        
        response = api_call('POST', '/stores', store_data, headers)
        
        if response and response.status_code == 201:
            flash('Store berhasil dibuat!', 'success')
            return redirect(url_for('store.stores'))
        else:
            flash('Gagal membuat store!', 'error')
    
    return render_template('store/create_store.html', 
    provinsis=provinsis)

@store_bp.route('/stores/<int:store_id>/edit', methods=['GET', 'POST'])
def edit_store(store_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}

    provinsi_response = api_wilayah_call('GET', '/provinces.json')
    provinsis = provinsi_response.json().get('data', []) if provinsi_response else []
    
    if request.method == 'POST':
        provinsi_code = request.form['provinsi_code']
        kabupaten_kota_code = request.form['kabupaten_kota_code']
        kecamatan_code = request.form['kecamatan_code']
        kelurahan_code = request.form['kelurahan_code']

        # ambil nama provinsi dari provinsis yang sudah di-load
        provinsi_name = next((provinsi['name'] for provinsi in provinsis if provinsi['code'] == provinsi_code), None)

        # ambil kabupaten via API
        kabupaten_kota_response = api_wilayah_call('GET', f'/regencies/{provinsi_code}.json')
        kabupaten_kotas = kabupaten_kota_response.json().get('data', []) if kabupaten_kota_response else []
        kabupaten_kota_name = next((kabupaten_kota['name'] for kabupaten_kota in kabupaten_kotas if kabupaten_kota['code'] == kabupaten_kota_code), None)

        # ambil kecamatan via API
        kecamatan_response = api_wilayah_call('GET', f'/districts/{kabupaten_kota_code}.json')
        kecamatans = kecamatan_response.json().get('data', []) if kecamatan_response else []
        kecamatan_name = next((kecamatan['name'] for kecamatan in kecamatans if kecamatan['code'] == kecamatan_code), None)

        # ambil kelurahan via API
        kelurahan_response = api_wilayah_call('GET', f'/villages/{kecamatan_code}.json')
        kelurahans = kelurahan_response.json().get('data', []) if kelurahan_response else []
        kelurahan_name = next((kelurahan['name'] for kelurahan in kelurahans if kelurahan['code'] == kelurahan_code), None)
        
        store_data = {
            'name': request.form['name'],
            'provinsi': provinsi_name,
            'kabupaten_kota': kabupaten_kota_name,
            'kecamatan': kecamatan_name,
            'kelurahan': kelurahan_name
        }
        
        response = api_call('PUT', f'/stores/{store_id}', store_data, headers)
        
        if response and response.status_code == 200:
            flash('Store berhasil diupdate!', 'success')
            return redirect(url_for('store.stores'))
        else:
            flash('Gagal mengupdate store!', 'error')
    
    store_response = api_call('GET', f'/stores/{store_id}', headers=headers)
    store = store_response.json() if store_response else {}
    
    return render_template('store/edit_store.html', store=store, provinsis=provinsis)

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