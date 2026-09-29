import streamlit as st
import sqlite3
import pandas as pd
import os
import base64
import hashlib

# 1. Configuración de la página web
st.set_page_config(
    page_title="BAYAMON TRUCK PARTS | CRM", 
    page_icon="🚛",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. GENERADOR DEL CAMIÓN SVG EN FORMATO BASE64
svg_truck_raw = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 85" width="170" height="72">
  <defs>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#2563eb" />
      <stop offset="100%" stop-color="#1d4ed8" />
    </linearGradient>
    <linearGradient id="metalGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f1f5f9" />
      <stop offset="100%" stop-color="#94a3b8" />
    </linearGradient>
  </defs>
  <rect x="5" y="14" width="105" height="46" rx="3" fill="#334155" stroke="#64748b" stroke-width="2" />
  <line x1="12" y1="22" x2="102" y2="22" stroke="#475569" stroke-width="1.5" />
  <line x1="12" y1="30" x2="102" y2="30" stroke="#475569" stroke-width="1.5" />
  <line x1="12" y1="38" x2="102" y2="38" stroke="#475569" stroke-width="1.5" />
  <line x1="12" y1="46" x2="102" y2="46" stroke="#475569" stroke-width="1.5" />
  <rect x="116" y="2" width="4" height="26" rx="2" fill="url(#metalGrad)" />
  <path d="M112 24 L132 12 L162 12 L185 34 L190 46 L190 62 L112 62 Z" fill="url(#bodyGrad)" stroke="#1e3a8a" stroke-width="1.5" />
  <path d="M158 16 L180 35 L160 35 L158 16 Z" fill="#ffffff" opacity="0.9" />
  <path d="M136 16 L154 16 L154 35 L136 35 Z" fill="#cbd5e1" opacity="0.85" />
  <rect x="186" y="42" width="6" height="18" rx="2" fill="url(#metalGrad)" />
  <rect x="183" y="58" width="11" height="6" rx="2" fill="#e2e8f0" />
  <circle cx="189" cy="50" r="3" fill="#fbbf24" />
  <rect x="120" y="50" width="22" height="10" rx="4" fill="url(#metalGrad)" />
  <circle cx="28" cy="64" r="10" fill="#0f172a" stroke="#94a3b8" stroke-width="2.5" />
  <circle cx="28" cy="64" r="4.5" fill="#f8fafc" />
  <circle cx="52" cy="64" r="10" fill="#0f172a" stroke="#94a3b8" stroke-width="2.5" />
  <circle cx="52" cy="64" r="4.5" fill="#f8fafc" />
  <circle cx="132" cy="64" r="10" fill="#0f172a" stroke="#94a3b8" stroke-width="2.5" />
  <circle cx="132" cy="64" r="4.5" fill="#f8fafc" />
  <circle cx="174" cy="64" r="10" fill="#0f172a" stroke="#94a3b8" stroke-width="2.5" />
  <circle cx="174" cy="64" r="4.5" fill="#f8fafc" />
</svg>"""

truck_base64 = base64.b64encode(svg_truck_raw.encode("utf-8")).decode("utf-8")

# 3. CSS GLOBAL: ESTILO MODERNO, ERGONÓMICO Y DE ALTO CONTRASTE
st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc !important;
        }

        /* Banner Hero Principal */
        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
            border: 1px solid #334155;
        }

        .hero-banner h1, .hero-banner .brand-title {
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            letter-spacing: 0.5px !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            margin: 0 !important;
            line-height: 1.2 !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
            white-space: nowrap;
        }

        .hero-banner p, .hero-banner .brand-subtitle {
            color: #93c5fd !important;
            -webkit-text-fill-color: #93c5fd !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin-top: 6px !important;
            letter-spacing: 0.2px !important;
        }

        /* Barra Lateral */
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 2px solid #cbd5e1 !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #0f172a !important;
            font-weight: 800 !important;
        }

        /* Tarjeta de Usuario Activo en la Barra Lateral */
        .user-badge {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* Campos de Entrada */
        input, select, textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid #64748b !important;
            border-radius: 6px !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }

        ::placeholder, input::placeholder, textarea::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
            font-weight: 500 !important;
        }

        label, .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
        }

        /* Botones de Acción */
        button, 
        .stButton > button, 
        button[data-testid="baseButton-primary"], 
        button[data-testid="baseButton-secondary"],
        .stFormSubmitButton > button {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: 1px solid #1d4ed8 !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
            padding: 0.5rem 1rem !important;
        }

        button p, .stButton > button p, button span, .stButton > button div {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        button:hover, .stButton > button:hover {
            background-color: #1d4ed8 !important;
            color: #ffffff !important;
            box-shadow: 0 6px 14px rgba(29, 78, 216, 0.4) !important;
        }

        /* Dropzone para archivos Excel */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #ffffff !important;
            border: 2px dashed #64748b !important;
            border-radius: 8px !important;
        }
        
        [data-testid="stFileUploaderDropzone"] * {
            color: #0f172a !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
        }

        /* Tarjetas de Métricas (KPIs) */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background-color: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            border-left: 5px solid #2563eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .kpi-label {
            font-size: 0.82rem;
            text-transform: uppercase;
            font-weight: 800;
            color: #475569 !important;
            letter-spacing: 0.5px;
        }

        .kpi-value {
            font-size: 1.8rem;
            font-weight: 900;
            color: #0f172a !important;
            margin-top: 2px;
        }

        /* Tarjeta Resumen de Contacto */
        .contact-card {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 8px;
            padding: 1.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }

        /* Notas de Seguimiento */
        .note-bubble {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #2563eb;
            border-radius: 6px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        
        .note-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .note-body {
            font-size: 0.95rem;
            color: #0f172a !important;
            font-weight: 500;
            line-height: 1.4;
        }
    </style>
""", unsafe_allow_html=True)

# 4. BASE DE DATOS Y GESTIÓN DE SEGURIDAD
DB_PATH = os.path.join(os.path.dirname(__file__), "crm.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT NOT NULL,
            sector TEXT,
            direccion TEXT
        );
        CREATE TABLE IF NOT EXISTS contactos (
            id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cargo TEXT,
            email TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );
        CREATE TABLE IF NOT EXISTS telefonos (
            id_telefono INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contacto INTEGER,
            numero_telefono TEXT NOT NULL,
            tipo TEXT,
            FOREIGN KEY (id_contacto) REFERENCES contactos(id_contacto)
        );
        CREATE TABLE IF NOT EXISTS notas (
            id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contacto INTEGER,
            autor TEXT DEFAULT 'Sistema',
            nota TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_contacto) REFERENCES contactos(id_contacto)
        );
    ''')
    
    # Migración de columna 'autor' si la tabla 'notas' ya existía previamente
    try:
        cursor.execute("ALTER TABLE notas ADD COLUMN autor TEXT DEFAULT 'Sistema'")
    except sqlite3.OperationalError:
        pass # La columna ya existe

    # Crear usuario administrador inicial si no hay usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (username, nombre_completo, password_hash, rol) VALUES (?, ?, ?, ?)",
            ("admin", "Administrador Principal", hash_password("admin123"), "Admin")
        )
    
    conexion.commit()
    conexion.close()

inicializar_db()

# 5. CONTROL DE SESIÓN (LOGIN)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = None
    st.session_state["nombre_completo"] = None
    st.session_state["rol"] = None

def autenticar_usuario(username, password):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id_usuario, username, nombre_completo, rol FROM usuarios WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password))
    )
    user = cursor.fetchone()
    conexion.close()
    return user

# ==========================================
# PANTALLA DE INICIO DE SESIÓN
# ==========================================
if not st.session_state["autenticado"]:
    col_izq, col_centro, col_der = st.columns([1, 1.4, 1])
    with col_centro:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <img src="data:image/svg+xml;base64,{truck_base64}" alt="Camión" style="max-width: 160px; margin: 0 auto; display: block;" />
                <h2 style="color: #0f172a; margin: 15px 0 5px 0; font-weight: 900; letter-spacing: -0.5px;">BAYAMON TRUCK PARTS</h2>
                <p style="color: #64748b; font-size: 0.95rem;">Acceso al CRM y Gestión de Clientes</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            usuario_input = st.text_input("Usuario", placeholder="Ingresa tu usuario...")
            password_input = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña...")
            btn_entrar = st.form_submit_button("Iniciar Sesión", use_container_width=True)

            if btn_entrar:
                datos_user = autenticar_usuario(usuario_input, password_input)
                if datos_user:
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = datos_user[1]
                    st.session_state["nombre_completo"] = datos_user[2]
                    st.session_state["rol"] = datos_user[3]
                    st.success("Acceso concedido.")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
        
        st.info("💡 **Primer acceso:** Usuario: `admin` | Contraseña: `admin123`")
    st.stop()

# ==========================================
# APLICACIÓN PRINCIPAL (USUARIO CONECTADO)
# ==========================================

def obtener_metricas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(DISTINCT id_cliente) FROM clientes")
    total_empresas = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM contactos")
    total_contactos = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM notas")
    total_notas = cursor.fetchone()[0] or 0
    conexion.close()
    return total_empresas, total_contactos, total_notas

total_empresas, total_contactos, total_notas = obtener_metricas()

# ENCABEZADO CON IDENTIDAD DE MARCA
st.markdown(f"""
<div class="hero-banner">
    <div>
        <h1 class="brand-title">BAYAMON TRUCK PARTS</h1>
        <p class="brand-subtitle">Gestión inteligente de relaciones y seguimiento comercial</p>
    </div>
    <div>
        <img src="data:image/svg+xml;base64,{truck_base64}" alt="Camión Heavy Duty" style="display: block; max-width: 170px; height: auto;" />
    </div>
</div>
""", unsafe_allow_html=True)

# FILA DE MÉTRICAS (KPIs)
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div>
            <div class="kpi-label">Empresas Clientes</div>
            <div class="kpi-value">{total_empresas}</div>
        </div>
        <div style="font-size: 2.2rem;">🏢</div>
    </div>
    <div class="kpi-card" style="border-left-color: #0284c7;">
        <div>
            <div class="kpi-label">Contactos Activos</div>
            <div class="kpi-value">{total_contactos}</div>
        </div>
        <div style="font-size: 2.2rem;">👥</div>
    </div>
    <div class="kpi-card" style="border-left-color: #d97706;">
        <div>
            <div class="kpi-label">Notas de Seguimiento</div>
            <div class="kpi-value">{total_notas}</div>
        </div>
        <div style="font-size: 2.2rem;">📝</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL: PERFIL, LOGOUT Y NUEVO CONTACTO
# ==========================================
st.sidebar.markdown(f"""
    <div class="user-badge">
        <div>
            <div style="font-size: 0.95rem; font-weight: 800; color: #0f172a;">👤 {st.session_state['nombre_completo']}</div>
            <div style="font-size: 0.8rem; color: #2563eb; font-weight: 600;">Rol: {st.session_state['rol']}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("Cerrar Sesión", use_container_width=True):
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = None
    st.session_state["rol"] = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ➕ Registrar Contacto")
with st.sidebar.form("form_contacto", clear_on_submit=True):
    empresa = st.text_input("Empresa *", placeholder="Ej: Transportes del Norte")
    sector = st.text_input("Sector", placeholder="Ej: Carga Pesada / Logística")
    nombre = st.text_input("Nombre *", placeholder="Ej: Carlos")
    apellido = st.text_input("Apellido *", placeholder="Ej: Rivera")
    cargo = st.text_input("Cargo", placeholder="Ej: Gerente de Flota")
    email = st.text_input("Email", placeholder="ejemplo@correo.com")
    telefono = st.text_input("Teléfono", placeholder="Ej: 787-555-0199")
    
    submit = st.form_submit_button("Guardar Registro", use_container_width=True)
    if submit:
        if not empresa.strip() or not nombre.strip() or not apellido.strip():
            st.sidebar.error("Empresa, Nombre y Apellido son obligatorios.")
        else:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                
                duplicado = False
                if telefono.strip():
                    cursor.execute("SELECT id_contacto FROM telefonos WHERE numero_telefono = ?", (telefono.strip(),))
                    if cursor.fetchone():
                        duplicado = True
                if email.strip() and not duplicado:
                    cursor.execute("SELECT id_contacto FROM contactos WHERE email = ?", (email.strip(),))
                    if cursor.fetchone():
                        duplicado = True

                if duplicado:
                    st.sidebar.warning("Este contacto ya existe (teléfono o email coinciden).")
                else:
                    cursor.execute("INSERT INTO clientes (nombre_empresa, sector) VALUES (?, ?)", (empresa.strip(), sector.strip()))
                    id_cliente = cursor.lastrowid
                    cursor.execute("INSERT INTO contactos (id_cliente, nombre, apellido, cargo, email) VALUES (?, ?, ?, ?, ?)", 
                                   (id_cliente, nombre.strip(), apellido.strip(), cargo.strip(), email.strip()))
                    id_contacto = cursor.lastrowid
                    if telefono.strip():
                        cursor.execute("INSERT INTO telefonos (id_contacto, numero_telefono, tipo) VALUES (?, ?, 'Trabajo')", 
                                       (id_contacto, telefono.strip()))
                    conexion.commit()
                    st.sidebar.success("¡Contacto guardado con éxito!")
                    st.rerun()
                conexion.close()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# SECCIÓN DE IMPORTACIÓN MASIVA
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Importación Masiva")
archivo_excel = st.sidebar.file_uploader("Cargar archivo .xlsx", type=["xlsx", "xls"])

if archivo_excel is not None:
    if st.sidebar.button("Procesar e Importar", use_container_width=True):
        try:
            df_import = pd.read_excel(archivo_excel)
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            importados = 0
            for _, row in df_import.iterrows():
                emp = str(row.get('Empresa', '')).strip()
                sec = str(row.get('Sector', '')).strip()
                nom = str(row.get('Nombre', '')).strip()
                ape = str(row.get('Apellido', '')).strip()
                car = str(row.get('Cargo', '')).strip()
                eml = str(row.get('Email', '')).strip()
                tel = str(row.get('Telefono', '')).strip()

                if not emp or not nom or not ape or emp == 'nan':
                    continue

                cursor.execute("INSERT INTO clientes (nombre_empresa, sector) VALUES (?, ?)", (emp, sec if sec != 'nan' else ''))
                id_cliente = cursor.lastrowid

                cursor.execute("INSERT INTO contactos (id_cliente, nombre, apellido, cargo, email) VALUES (?, ?, ?, ?, ?)", 
                               (id_cliente, nom, ape, car if car != 'nan' else '', eml if eml != 'nan' else ''))
                id_contacto = cursor.lastrowid

                if tel and tel != 'nan':
                    cursor.execute("INSERT INTO telefonos (id_contacto, numero_telefono, tipo) VALUES (?, ?, 'Trabajo')", 
                                   (id_contacto, tel))
                
                importados += 1

            conexion.commit()
            conexion.close()
            st.sidebar.success(f"Se importaron {importados} contactos exitosamente.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error al procesar archivo: {e}")

# ==========================================
# PESTAÑAS PRINCIPALES (CON GESTIÓN DE USUARIOS)
# ==========================================
pestanas_nombres = ["📋 Directorio y Notas", "✏️ Modificar Registros"]
if st.session_state["rol"] == "Admin":
    pestanas_nombres.append("👥 Gestión de Usuarios")

pestanas = st.tabs(pestanas_nombres)

# ------------------------------------------
# PESTAÑA 1: DIRECTORIO, BÚSQUEDA Y NOTAS
# ------------------------------------------
with pestanas[0]:
    filtro = st.text_input("Buscador Central", placeholder="🔍 Buscar por empresa, nombre, cargo, teléfono, email...", label_visibility="collapsed")

    conexion = conectar_db()
    cursor = conexion.cursor()

    query = '''
        SELECT c.id_contacto, cl.nombre_empresa, cl.sector, c.nombre, c.apellido, c.cargo, c.email, t.numero_telefono 
        FROM clientes cl
        JOIN contactos c ON cl.id_cliente = c.id_cliente
        LEFT JOIN telefonos t ON c.id_contacto = t.id_contacto
    '''

    if filtro:
        query += ''' WHERE cl.nombre_empresa LIKE ? 
                   OR cl.sector LIKE ? 
                   OR c.nombre LIKE ? 
                   OR c.apellido LIKE ? 
                   OR c.cargo LIKE ? 
                   OR c.email LIKE ?
                   OR t.numero_telefono LIKE ?'''
        param = f"%{filtro}%"
        cursor.execute(query, (param, param, param, param, param, param, param))
    else:
        cursor.execute(query)

    filas = cursor.fetchall()
    conexion.close()

    if filas:
        df = pd.DataFrame(filas, columns=["ID", "Empresa", "Sector", "Nombre", "Apellido", "Cargo", "Email", "Teléfono"])
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True, height=260, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💬 Bitácora y Seguimiento Comercial")
        
        nombres_opciones = {f"{row[3]} {row[4]} — {row[1]}": row[0] for row in filas}
        seleccion_contacto = st.selectbox("Seleccionar contacto para ver historial:", options=list(nombres_opciones.keys()))
        
        if seleccion_contacto:
            id_sel = nombres_opciones[seleccion_contacto]
            datos_sel = next(r for r in filas if r[0] == id_sel)
            _, s_emp, s_sec, s_nom, s_ape, s_cargo, s_email, s_tel = datos_sel

            st.markdown(f"""
                <div class="contact-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <h3 style="margin: 0; color: #0f172a; font-size: 1.3rem; font-weight: 800;">{s_nom} {s_ape}</h3>
                            <p style="margin: 4px 0 0 0; color: #334155; font-weight: 700;">{s_emp} &nbsp;•&nbsp; <span style="color:#2563eb;">{s_cargo or 'Sin cargo'}</span></p>
                            <p style="margin: 3px 0 0 0; color: #64748b; font-size: 0.9rem;">Sector: {s_sec or 'General'}</p>
                        </div>
                        <div style="text-align: right; font-size: 0.95rem; margin-top: 5px;">
                            <div style="color: #0f172a;">📞 <strong>{s_tel or 'Sin teléfono'}</strong></div>
                            <div style="color: #0f172a;">✉️ <strong>{s_email or 'Sin correo'}</strong></div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col_historial, col_nueva_nota = st.columns([1.2, 1])

            with col_historial:
                st.markdown("#### Historial de Interacciones")
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("SELECT fecha, autor, nota FROM notas WHERE id_contacto = ? ORDER BY fecha DESC", (id_sel,))
                notas = cursor.fetchall()
                conexion.close()

                if notas:
                    for fecha, autor, nota in notas:
                        st.markdown(f"""
                            <div class="note-bubble">
                                <div class="note-meta">
                                    <span style="color: #2563eb;">📅 {fecha}</span>
                                    <span style="color: #64748b;">👤 Por: <strong>{autor or 'Desconocido'}</strong></span>
                                </div>
                                <div class="note-body">{nota}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No hay notas previas registradas para este contacto.")

            with col_nueva_nota:
                st.markdown("#### Registrar Nueva Nota")
                with st.form("form_nota", clear_on_submit=True):
                    nueva_nota = st.text_area(
                        "Detalles de la conversación o acuerdo:", 
                        placeholder="Ej: Se coordinó entrega de repuestos para el martes...",
                        height=120
                    )
                    submit_nota = st.form_submit_button("Guardar Nota", use_container_width=True)
                    if submit_nota and nueva_nota.strip():
                        conexion = conectar_db()
                        cursor = conexion.cursor()
                        cursor.execute(
                            "INSERT INTO notas (id_contacto, autor, nota) VALUES (?, ?, ?)", 
                            (id_sel, st.session_state["nombre_completo"], nueva_nota.strip())
                        )
                        conexion.commit()
                        conexion.close()
                        st.success("Nota agregada correctamente.")
                        st.rerun()
    else:
        st.info("No se encontraron registros activos.")

# ------------------------------------------
# PESTAÑA 2: MODIFICAR / EDITAR CONTACTOS
# ------------------------------------------
with pestanas[1]:
    st.markdown("### Modificar Datos de Contacto y Empresa")
    
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT c.id_contacto, cl.nombre_empresa, c.nombre, c.apellido, c.email 
        FROM clientes cl
        JOIN contactos c ON cl.id_cliente = c.id_cliente
    ''')
    todos_contactos = cursor.fetchall()
    conexion.close()

    if todos_contactos:
        dict_edit = {f"{row[2]} {row[3]} — {row[1]} ({row[4] or 'Sin email'})": row[0] for row in todos_contactos}
        contacto_a_editar = st.selectbox("Seleccione el contacto que desea actualizar:", options=list(dict_edit.keys()))

        if contacto_a_editar:
            id_editar = dict_edit[contacto_a_editar]

            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT cl.nombre_empresa, cl.sector, c.nombre, c.apellido, c.cargo, c.email, t.numero_telefono, cl.id_cliente, t.id_telefono
                FROM clientes cl
                JOIN contactos c ON cl.id_cliente = c.id_cliente
                LEFT JOIN telefonos t ON c.id_contacto = t.id_contacto
                WHERE c.id_contacto = ?
            ''', (id_editar,))
            datos_actuales = cursor.fetchone()
            conexion.close()

            if datos_actuales:
                e_empresa, e_sector, e_nombre, e_apellido, e_cargo, e_email, e_telefono, id_cliente, id_telefono = datos_actuales

                with st.form("form_edicion"):
                    st.markdown("##### Información Comercial")
                    col1, col2 = st.columns(2)
                    with col1:
                        nuevo_empresa = st.text_input("Empresa *", value=str(e_empresa or ""))
                        nuevo_sector = st.text_input("Sector Industrial", value=str(e_sector or ""))
                    with col2:
                        nuevo_cargo = st.text_input("Cargo del Contacto", value=str(e_cargo or ""))
                    
                    st.markdown("##### Información Personal")
                    col3, col4 = st.columns(2)
                    with col3:
                        nuevo_nombre = st.text_input("Nombre *", value=str(e_nombre or ""))
                        nuevo_email = st.text_input("Correo Electrónico", value=str(e_email or ""))
                    with col4:
                        nuevo_apellido = st.text_input("Apellido *", value=str(e_apellido or ""))
                        nuevo_telefono = st.text_input("Teléfono", value=str(e_telefono or ""))

                    st.markdown("<br>", unsafe_allow_html=True)
                    btn_actualizar = st.form_submit_button("Guardar Cambios Actualizados", use_container_width=True)

                    if btn_actualizar:
                        if not nuevo_empresa.strip() or not nuevo_nombre.strip() or not nuevo_apellido.strip():
                            st.error("Empresa, Nombre y Apellido no pueden quedar vacíos.")
                        else:
                            try:
                                conexion = conectar_db()
                                cursor = conexion.cursor()
                                
                                cursor.execute("UPDATE clientes SET nombre_empresa = ?, sector = ? WHERE id_cliente = ?", 
                                               (nuevo_empresa.strip(), nuevo_sector.strip(), id_cliente))
                                cursor.execute("UPDATE contactos SET nombre = ?, apellido = ?, cargo = ?, email = ? WHERE id_contacto = ?", 
                                               (nuevo_nombre.strip(), nuevo_apellido.strip(), nuevo_cargo.strip(), nuevo_email.strip(), id_editar))
                                
                                if id_telefono:
                                    cursor.execute("UPDATE telefonos SET numero_telefono = ? WHERE id_telefono = ?", 
                                                   (nuevo_telefono.strip(), id_telefono))
                                elif nuevo_telefono.strip():
                                    cursor.execute("INSERT INTO telefonos (id_contacto, numero_telefono, tipo) VALUES (?, ?, 'Trabajo')", 
                                                   (id_editar, nuevo_telefono.strip()))

                                conexion.commit()
                                conexion.close()
                                st.success("Registro actualizado exitosamente.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al actualizar: {e}")
    else:
        st.info("No hay contactos disponibles para modificar.")

# ------------------------------------------
# PESTAÑA 3: GESTIÓN DE USUARIOS (SOLO ADMIN)
# ------------------------------------------
if st.session_state["rol"] == "Admin":
    with pestanas[2]:
        st.markdown("### 👥 Administración de Usuarios del CRM")
        
        col_listado, col_crear = st.columns([1.3, 1])

        with col_listado:
            st.markdown("#### Usuarios Activos")
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_usuario, username, nombre_completo, rol, fecha_creacion FROM usuarios")
            usuarios_db = cursor.fetchall()
            conexion.close()

            if usuarios_db:
                df_usuarios = pd.DataFrame(usuarios_db, columns=["ID", "Usuario", "Nombre Completo", "Rol", "Fecha de Alta"])
                st.dataframe(df_usuarios.drop(columns=["ID"]), use_container_width=True, hide_index=True)

        with col_crear:
            st.markdown("#### Crear Nuevo Acceso")
            with st.form("form_nuevo_usuario", clear_on_submit=True):
                nuevo_user = st.text_input("Usuario (Login) *", placeholder="Ej: crivera")
                nuevo_nombre = st.text_input("Nombre y Apellido *", placeholder="Ej: Carlos Rivera")
                nuevo_pass = st.text_input("Contraseña *", type="password", placeholder="Contraseña segura...")
                nuevo_rol = st.selectbox("Rol de Usuario", options=["Vendedor", "Admin"])
                
                btn_crear_user = st.form_submit_button("Crear Usuario", use_container_width=True)
                if btn_crear_user:
                    if not nuevo_user.strip() or not nuevo_nombre.strip() or not nuevo_pass.strip():
                        st.error("Todos los campos marcados con * son obligatorios.")
                    else:
                        try:
                            conexion = conectar_db()
                            cursor = conexion.cursor()
                            cursor.execute(
                                "INSERT INTO usuarios (username, nombre_completo, password_hash, rol) VALUES (?, ?, ?, ?)",
                                (nuevo_user.strip().lower(), nuevo_nombre.strip(), hash_password(nuevo_pass), nuevo_rol)
                            )
                            conexion.commit()
                            conexion.close()
                            st.success(f"Usuario '{nuevo_user}' creado exitosamente.")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Ese nombre de usuario ya existe. Elige otro.")
                        except Exception as e:
                            st.error(f"Error al crear usuario: {e}")