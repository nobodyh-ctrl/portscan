
# 🔍 PortScan — Escáner de Puertos TCP
<div align="center">

[![Python](https://img.shields.io/badge/PYTHON-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TCP/IP](https://img.shields.io/badge/TCP%2FIP-blue?style=for-the-badge&logoColor=white)](https://en.wikipedia.org/wiki/Internet_protocol_suite)
[![Cybersecurity](https://img.shields.io/badge/CYBERSECURITY-red?style=for-the-badge&logoColor=white)](https://owasp.org/)
[![Open Source](https://img.shields.io/badge/OPEN%20SOURCE-yellow?style=for-the-badge&logoColor=black)](https://opensource.org/licenses/MIT)

</div>

**PortScan** es una herramienta de línea de comandos que escanea rangos de puertos TCP sobre una IP objetivo, construida **desde cero** (sin depender de `nmap` ni de ninguna librería de escaneo) como proyecto educativo para aprender los fundamentos de **Networking** y **Ciberseguridad**.

## 📖 ¿Qué es PortScan?

PortScan recibe una dirección IP y un rango de puertos, intenta establecer una conexión TCP con cada uno, y clasifica el resultado en tres estados: **OPEN**, **CLOSED** o **FILTERED**. No es un reemplazo de herramientas profesionales como `nmap` — es intencionalmente simple, para que cada línea de código sea entendible y quede claro **qué pasa realmente en la red** en cada paso, sin abstracciones que oculten el mecanismo.

Es un proyecto **open source**, pensado para compartirse con la comunidad de ciberseguridad y networking: cualquiera puede leer el código, entender el porqué de cada decisión, y usarlo como punto de partida para su propio aprendizaje.

## 👥 ¿Para quién está pensado?

- Estudiantes que están dando sus primeros pasos en **Networking** y **Ciberseguridad**.
- Profesionales de IT que quieren entender qué hay realmente "debajo" de herramientas como `nmap`.
- Personas orientando su carrera hacia **SOC / Blue Team**, **infraestructura** o **administración de redes**, que necesitan una base sólida de cómo funciona TCP/IP a nivel práctico.

## 🧠 Conceptos de Networking y Seguridad detrás del proyecto

| Concepto | Resumen |
|---|---|
| **Dirección IP** | Identifica un dispositivo dentro de una red. |
| **Puerto** | Identifica un servicio específico dentro de ese dispositivo. |
| **TCP y el three-way handshake** | Antes de intercambiar datos, dos dispositivos confirman la conexión con `SYN → SYN-ACK → ACK`. |
| **Socket** | La interfaz que el sistema operativo expone para crear conexiones de red. |
| **OPEN** | El destino respondió `SYN-ACK`: hay un servicio escuchando en ese puerto. |
| **CLOSED** | El destino respondió `RST`: no hay ningún servicio escuchando, pero el tráfico llegó. |
| **FILTERED** | No hubo ninguna respuesta dentro del tiempo de espera — típicamente porque un **firewall** descartó el paquete en silencio (política de **default deny**). |
| **Network Reconnaissance** | El proceso de descubrir qué servicios están expuestos en una red, base de cualquier auditoría de seguridad o administración de infraestructura. |

Estos conceptos se entienden mejor de forma práctica que teórica — en la sección de laboratorio más abajo explico cómo reproducir cada estado con una VM propia.

## ⚙️ Cómo funciona (resumen técnico)

Por cada puerto del rango, PortScan:

1. Crea un socket TCP (`AF_INET`, `SOCK_STREAM`).
2. Le asigna un timeout, para no quedarse esperando indefinidamente ante un puerto sin respuesta.
3. Llama a `connect_ex()`, que intenta el handshake TCP y devuelve un código en vez de lanzar una excepción.
4. Clasifica el resultado:
   - `0` → **OPEN**
   - `errno.ECONNREFUSED` (el sistema operativo destino respondió con RST) → **CLOSED**
   - Cualquier otro caso (se agotó el timeout sin respuesta) → **FILTERED**

El escaneo del rango está implementado como un **generador de Python**, que va entregando el resultado puerto por puerto a medida que lo obtiene, en lugar de esperar a tener todo el rango escaneado para mostrar algo — esto permite ver el progreso en tiempo real en rangos grandes.

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|---|---|
| [Python 3](https://www.python.org/) | Lenguaje del proyecto. |
| [`socket`](https://docs.python.org/3/library/socket.html) | Módulo estándar para crear conexiones TCP (núcleo del scanner). |
| [`errno`](https://docs.python.org/3/library/errno.html) | Códigos de error portables entre sistemas operativos. |
| [`argparse`](https://docs.python.org/3/library/argparse.html) | Parseo de argumentos de línea de comandos. |
| [`pyfiglet`](https://pypi.org/project/pyfiglet/) | Generación del banner ASCII art. |
| [`setuptools` / `pyproject.toml`](https://setuptools.pypa.io/) | Empaquetado del proyecto como comando instalable (`portscan`). |

## 📦 Instalación

### Requisitos previos

- **Python 3.8 o superior**
- **pip** (viene incluido con Python 3.4+; en algunas distros de Linux es un paquete aparte, ver abajo)
- **git** (para clonar el repositorio)

PortScan no tiene dependencias externas del sistema operativo — todo lo que necesita es Python y las librerías declaradas en `pyproject.toml` (se instalan solas con `pip`).

### Clonar el repositorio

```bash
git clone <url-de-este-repositorio>
cd network-scanner
```

### Windows

```powershell
pip install -e .
```

> Si la terminal no reconoce el comando `portscan` después de instalar, puede que la carpeta `Scripts` de tu instalación de Python no esté en el `PATH` de Windows. `pip install` te avisa la ruta exacta en un mensaje de warning — agregala a tu `PATH` (Variables de entorno de tu usuario) y abrí una terminal nueva.

### Linux / macOS

En distribuciones recientes de Ubuntu/Debian, `pip` puede rechazar instalar paquetes directamente sobre el Python del sistema (protección **PEP 668**, "externally managed environment"). Hay dos formas válidas de instalar, según qué necesites:

**Opción A — `venv` (entorno aislado, solo activo cuando lo activás):**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Con esto, el comando `portscan` **solo funciona mientras ese entorno virtual esté activado** en la terminal (`source venv/bin/activate`). Si abrís una terminal nueva o no lo activás, `portscan` no se va a encontrar — no es un error, es cómo funcionan los entornos virtuales por diseño (aíslan dependencias por proyecto).

**Opción B — `pipx` (comando disponible siempre, sin activar nada) — recomendada si querés usarlo como herramienta de sistema, tipo `nmap`:**

```bash
sudo apt install pipx   # si no lo tenés instalado
pipx install .
```

`pipx` instala el paquete en un entorno aislado igual que `venv`, pero además deja el comando (`portscan`) enlazado en una carpeta que sí queda en tu `PATH` (normalmente `~/.local/bin`), así que funciona en cualquier terminal nueva sin pasos extra.

## 🚀 Uso

```bash
portscan -t <IP_OBJETIVO> -s <PUERTO_INICIAL> -e <PUERTO_FINAL>
```

| Flag | Descripción |
|---|---|
| `-t`, `--target` | Dirección IP a escanear. |
| `-s`, `--start` | Puerto inicial del rango. |
| `-e`, `--end` | Puerto final del rango. |

### Ejemplo

```bash
portscan -t 192.168.1.10 -s 1 -e 1000
```

### Salida de ejemplo

```
PORT    STATUS
------------------
22      OPEN
80      OPEN
443     OPEN
3306    CLOSED
8080    FILTERED
------------------
Puertos abiertos: 22, 80, 443

Resultados guardados en: C:\Users\<usuario>\portscan_results\scan_192.168.1.10_20260830_131134.txt
```

Cada escaneo además se guarda automáticamente como archivo de texto en `~/portscan_results/`, con la IP, el rango y la fecha, sin importar desde qué carpeta hayas ejecutado el comando.

## 🗂️ Estructura del proyecto

```
network-scanner/
├── pyproject.toml       # Metadata del paquete + entry point del comando "portscan"
├── README.md
├── LICENSE
└── portscan/
    ├── cli.py           # Parseo de argumentos y orquestación general
    ├── scanner.py       # Lógica de sockets/TCP (el corazón del scanner)
    ├── display.py       # Formato e impresión de resultados en pantalla
    ├── banner.py        # Banner ASCII art
    └── report.py        # Guardado de resultados en ~/portscan_results/
```

Cada archivo tiene una única responsabilidad: la lógica de red no sabe nada sobre cómo se imprime en pantalla ni cómo se guarda un reporte, lo que permite modificar una parte sin tocar las demás.

## 🧪 Laboratorio de pruebas

Este proyecto se desarrolló y probó usando un laboratorio local simple:

```
PC (Windows) ──── LAN ──── VM Ubuntu Server (VirtualBox, adaptador Bridged)
```

- El puerto **OPEN** se probó con el servicio SSH real corriendo en la VM (puerto 22).
- El puerto **CLOSED** se probó permitiendo tráfico con `ufw allow` hacia un puerto sin ningún servicio escuchando.
- El puerto **FILTERED** se probó bloqueando tráfico en silencio con `ufw deny` (política de firewall tipo DROP).

Este entorno es reproducible con cualquier hipervisor (VirtualBox, VMware) y una VM Linux liviana.

## 🔧 Troubleshooting

### Firewalls "en capas" (Windows)

En Windows, agregar una regla de entrada en el Firewall de Windows (`New-NetFirewallRule ... -Action Allow`) **no garantiza** que el puerto pase a OPEN. Muchos antivirus/suites de seguridad (Avast, Norton, McAfee, etc.) traen su **propio módulo de firewall**, que filtra el tráfico de forma independiente y adicional al Firewall de Windows — si ese módulo bloquea el puerto, va a seguir dando **FILTERED** aunque la regla de Windows Firewall esté perfectamente configurada (`Enabled: True`, `Action: Allow`).

Ejemplo real detectado durante el desarrollo de este proyecto: al intentar exponer un servidor MySQL local en el puerto 3306 para escanearlo desde otra máquina de la LAN, la regla de Windows Firewall no alcanzó — **Avast Antivirus** seguía bloqueando el tráfico entrante en su propio firewall, hasta agregar la excepción correspondiente también ahí.

**Si agregaste una regla de firewall y el puerto sigue en FILTERED:** revisá si tenés un antivirus con firewall propio instalado, y agregá la excepción ahí también.

### `ImportError: cannot import name 'main' from 'portscan.cli'` al instalar con `pipx`

En algunos entornos (detectado con `pipx` 1.8.0 sobre Python 3.14), `pipx install .` puede terminar instalando un `cli.py` **vacío** dentro de su entorno interno, aunque el comando reporte que la instalación fue exitosa. Es un bug de cómo `pipx` arma el paquete al construirlo directamente desde una carpeta fuente — no afecta al código en sí ni a una instalación con `pip`/`venv` normal.

**Solución:** construir el `wheel` (el paquete ya empaquetado) vos mismo con `build`, e instalar ese archivo en vez de la carpeta fuente:

```bash
python3 -m venv build-venv
build-venv/bin/pip install build
build-venv/bin/python -m build
pipx uninstall portscan   # si había quedado una instalación rota
pipx install dist/*.whl
rm -rf build-venv
```

## ⚠️ Limitaciones (v1)

- **Escaneo secuencial**, no concurrente: escanear rangos grandes puede ser lento, especialmente si hay muchos puertos FILTERED (cada uno consume el timeout completo).
- **Timeout fijo**: en redes con latencia variable, un timeout corto puede confundir un puerto CLOSED real con FILTERED.
- **Solo TCP**: no incluye escaneo UDP.
- **Sin detección de servicios ni versiones**: solo determina el estado del puerto, no qué software corre detrás.
- **El resultado depende del punto de observación**: software de seguridad local (antivirus, firewalls corporativos) puede interceptar ciertos puertos y alterar el resultado — por ejemplo, es común que el puerto 25 (SMTP) sea interceptado activamente por software antispam, generando falsos positivos de "OPEN".

## 🤝 Contribuciones

Este es un proyecto open source y educativo — las contribuciones, sugerencias e issues son bienvenidos. Si estás empezando en Networking o Ciberseguridad como yo, sentite libre de forkearlo, romperlo, y usarlo para aprender.

## ⚖️ Uso responsable

PortScan está pensado con fines **educativos** y de **administración de redes propias**. Escanear dispositivos o redes sin autorización explícita puede ser ilegal según la jurisdicción. Usá esta herramienta únicamente sobre sistemas de tu propiedad o con permiso explícito del propietario.

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
