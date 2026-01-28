"""
PROGRAMA DE TRANSFERENCIA DE ARCHIVOS USB
==========================================
Simula la transferencia de un archivo de texto entre dos computadoras
conectadas por USB, mostrando el proceso a nivel de lenguaje de máquina.
"""

import time
import os
from typing import List

# Colores ANSI para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(texto: str):
    """Imprime un título formateado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{texto.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def char_a_binario(char: str) -> str:
    """Convierte un carácter a su representación binaria (8 bits)"""
    return format(ord(char), '08b')

def char_a_hex(char: str) -> str:
    """Convierte un carácter a su representación hexadecimal"""
    return format(ord(char), '02X')

def simular_escritura(texto: str, delay: float = 0.03):
    """Simula escritura caracter por caracter"""
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# ============================================================================
# PROGRAMA COMPUTADORA EMISORA (ORIGEN)
# ============================================================================

class ComputadoraEmisor:
    """
    Representa la computadora que envía el archivo.
    Componentes:
    - CPU: Procesa las instrucciones
    - Memoria RAM: Almacena temporalmente los datos
    - Controlador USB: Gestiona la comunicación USB
    - Sistema de Archivos: Lee el archivo del disco
    """
    
    def __init__(self):
        self.buffer_memoria = []
        self.puerto_usb = None
        self.archivo_origen = "archivo_a.txt"
        
    def crear_archivo_origen(self):
        """PASO 1: Crear archivo de texto con la letra 'a'"""
        imprimir_titulo("COMPUTADORA EMISORA - PASO 1: Crear Archivo")
        
        print(f"{Colors.YELLOW}📄 Creando archivo '{self.archivo_origen}' con contenido 'a'{Colors.END}")
        with open(self.archivo_origen, 'w') as f:
            f.write('a')
        
        print(f"{Colors.GREEN}✓ Archivo creado exitosamente{Colors.END}")
        time.sleep(1)
    
    def leer_archivo(self) -> str:
        """PASO 2: Leer archivo desde el disco"""
        imprimir_titulo("COMPUTADORA EMISORA - PASO 2: Lectura del Archivo")
        
        print(f"{Colors.YELLOW}💾 INSTRUCCIONES EN LENGUAJE DE MÁQUINA:{Colors.END}\n")
        
        # Simulación de instrucciones en lenguaje de máquina
        instrucciones = [
            ("10110000 00000001", "MOV AL, 1", "Cargar handle del archivo en AL"),
            ("10001101 00011110", "LEA BX, [filename]", "Cargar dirección del nombre del archivo"),
            ("10110100 00111101", "MOV AH, 3Dh", "Función de apertura de archivo"),
            ("11001101 00100001", "INT 21h", "Llamada al sistema DOS"),
            ("10110100 00111111", "MOV AH, 3Fh", "Función de lectura de archivo"),
            ("10111001 00000001", "MOV CX, 1", "Leer 1 byte"),
            ("11001101 00100001", "INT 21h", "Llamada al sistema - Leer"),
        ]
        
        for binario, asm, descripcion in instrucciones:
            print(f"{Colors.CYAN}{binario}{Colors.END} → {Colors.YELLOW}{asm:20s}{Colors.END} ; {descripcion}")
            time.sleep(0.5)
        
        with open(self.archivo_origen, 'r') as f:
            contenido = f.read()
        
        print(f"\n{Colors.GREEN}✓ Contenido leído: '{contenido}'{Colors.END}")
        time.sleep(1)
        return contenido
    
    def cargar_en_memoria(self, datos: str):
        """PASO 3: Cargar datos en memoria RAM"""
        imprimir_titulo("COMPUTADORA EMISORA - PASO 3: Carga en Memoria RAM")
        
        print(f"{Colors.YELLOW}🧠 PROCESO DE CARGA EN MEMORIA:{Colors.END}\n")
        
        for char in datos:
            binario = char_a_binario(char)
            hex_val = char_a_hex(char)
            ascii_val = ord(char)
            
            print(f"Carácter: '{char}'")
            print(f"  └─ ASCII Decimal: {ascii_val}")
            print(f"  └─ Hexadecimal:   0x{hex_val}")
            print(f"  └─ Binario:       {binario}")
            
            self.buffer_memoria.append({
                'char': char,
                'ascii': ascii_val,
                'hex': hex_val,
                'binario': binario
            })
            
            # Instrucciones de almacenamiento
            print(f"\n{Colors.CYAN}Instrucciones de máquina:{Colors.END}")
            print(f"  {Colors.CYAN}10110000 {binario[:4]} {binario[4:]}{Colors.END} → MOV AL, {hex_val}h")
            print(f"  {Colors.CYAN}10100010 00000000 00010000{Colors.END} → MOV [1000h], AL")
            print(f"{Colors.GREEN}✓ Byte almacenado en dirección de memoria 0x1000{Colors.END}\n")
            time.sleep(1)
    
    def preparar_transmision_usb(self):
        """PASO 4: Preparar puerto USB para transmisión"""
        imprimir_titulo("COMPUTADORA EMISORA - PASO 4: Configuración USB")
        
        print(f"{Colors.YELLOW}🔌 INICIALIZACIÓN DEL CONTROLADOR USB:{Colors.END}\n")
        
        instrucciones_usb = [
            ("11100100 01100000", "IN AL, 60h", "Leer estado del puerto USB"),
            ("00001100 00000001", "OR AL, 01h", "Activar bit de habilitación USB"),
            ("11100110 01100000", "OUT 60h, AL", "Escribir configuración al puerto"),
            ("10111010 00111000 00000100", "MOV DX, 0438h", "Dirección base del controlador USB"),
            ("10110000 00000001", "MOV AL, 01h", "Modo de transmisión"),
            ("11101110", "OUT DX, AL", "Configurar modo USB"),
        ]
        
        for binario, asm, descripcion in instrucciones_usb:
            print(f"{Colors.CYAN}{binario:30s}{Colors.END} → {asm:25s} ; {descripcion}")
            time.sleep(0.5)
        
        print(f"\n{Colors.GREEN}✓ Puerto USB configurado y listo para transmitir{Colors.END}")
        time.sleep(1)
    
    def transmitir_datos(self) -> List[dict]:
        """PASO 5: Transmitir datos por USB"""
        imprimir_titulo("COMPUTADORA EMISORA - PASO 5: Transmisión USB")
        
        print(f"{Colors.YELLOW}📡 TRANSMITIENDO DATOS POR CABLE USB:{Colors.END}\n")
        
        for i, byte_data in enumerate(self.buffer_memoria):
            print(f"Paquete #{i+1}:")
            print(f"  Dato: '{byte_data['char']}' (0x{byte_data['hex']})")
            print(f"  Binario: {byte_data['binario']}")
            
            # Simulación de instrucciones de transmisión
            print(f"\n{Colors.CYAN}  Instrucciones de transmisión:{Colors.END}")
            print(f"  {Colors.CYAN}10100000 00000000 00010000{Colors.END} → MOV AL, [1000h]    ; Cargar byte de memoria")
            print(f"  {Colors.CYAN}10111010 11111000 00000011{Colors.END} → MOV DX, 03F8h     ; Puerto USB de salida")
            print(f"  {Colors.CYAN}11101110{Colors.END}                     → OUT DX, AL       ; Enviar byte por USB")
            
            # Animación de transmisión
            print(f"\n  {Colors.YELLOW}Enviando", end='')
            for _ in range(5):
                print('.', end='', flush=True)
                time.sleep(0.2)
            print(f" {Colors.GREEN}✓ Transmitido{Colors.END}\n")
        
        return self.buffer_memoria


# ============================================================================
# CANAL USB (MEDIO DE TRANSMISIÓN)
# ============================================================================

class CanalUSB:
    """
    Representa el cable USB y el protocolo de comunicación.
    Componentes:
    - Cable físico (4 hilos: VCC, GND, D+, D-)
    - Protocolo USB
    - Control de errores (CRC)
    """
    
    def __init__(self):
        self.paquetes_en_transito = []
    
    def transmitir(self, datos: List[dict]):
        """Simula la transmisión por el cable USB"""
        imprimir_titulo("CANAL USB - Transmisión de Datos")
        
        print(f"{Colors.YELLOW}🔗 PROTOCOLO USB - CAPA FÍSICA:{Colors.END}\n")
        print("Cable USB (4 hilos):")
        print("  🔴 VCC  → Alimentación (+5V)")
        print("  ⚫ GND  → Tierra (0V)")
        print("  🟢 D+   → Datos positivo")
        print("  ⚪ D-   → Datos negativo\n")
        
        for dato in datos:
            print(f"{Colors.YELLOW}Transmitiendo por líneas D+/D-:{Colors.END}")
            binario = dato['binario']
            
            # Mostrar transmisión bit por bit
            print("  Bits: ", end='')
            for bit in binario:
                color = Colors.GREEN if bit == '1' else Colors.RED
                print(f"{color}{bit}{Colors.END}", end=' ')
                time.sleep(0.1)
            
            # Calcular CRC (simplificado)
            crc = sum([int(b) for b in binario]) % 256
            print(f"\n  CRC: {format(crc, '08b')} (control de errores)")
            print(f"{Colors.GREEN}✓ Paquete verificado{Colors.END}\n")
            
            self.paquetes_en_transito.append(dato)
            time.sleep(0.5)
        
        return self.paquetes_en_transito


# ============================================================================
# PROGRAMA COMPUTADORA RECEPTORA (DESTINO)
# ============================================================================

class ComputadoraReceptor:
    """
    Representa la computadora que recibe el archivo.
    Componentes:
    - Controlador USB: Recibe los datos
    - Memoria RAM: Almacena temporalmente los datos
    - CPU: Procesa las instrucciones
    - Sistema de Archivos: Escribe el archivo en disco
    """
    
    def __init__(self):
        self.buffer_recepcion = []
        self.archivo_destino = "archivo_recibido.txt"
    
    def recibir_datos_usb(self, paquetes: List[dict]):
        """PASO 1: Recibir datos del puerto USB"""
        imprimir_titulo("COMPUTADORA RECEPTORA - PASO 1: Recepción USB")
        
        print(f"{Colors.YELLOW}📥 RECIBIENDO DATOS DEL PUERTO USB:{Colors.END}\n")
        
        instrucciones_rx = [
            ("10111010 11111000 00000011", "MOV DX, 03F8h", "Puerto USB de entrada"),
            ("11101100", "IN AL, DX", "Leer byte del puerto USB"),
            ("00111100 00000000", "CMP AL, 0", "Verificar si hay datos"),
            ("01110100 11111010", "JE RX_WAIT", "Esperar si no hay datos"),
        ]
        
        for binario, asm, descripcion in instrucciones_rx:
            print(f"{Colors.CYAN}{binario:30s}{Colors.END} → {asm:25s} ; {descripcion}")
            time.sleep(0.5)
        
        print()
        for paquete in paquetes:
            print(f"Recibido: '{paquete['char']}' → {paquete['binario']} (0x{paquete['hex']})")
            self.buffer_recepcion.append(paquete)
            time.sleep(0.5)
        
        print(f"\n{Colors.GREEN}✓ Todos los datos recibidos correctamente{Colors.END}")
        time.sleep(1)
    
    def almacenar_en_memoria(self):
        """PASO 2: Almacenar en memoria RAM"""
        imprimir_titulo("COMPUTADORA RECEPTORA - PASO 2: Almacenamiento en RAM")
        
        print(f"{Colors.YELLOW}🧠 GUARDANDO EN MEMORIA RAM:{Colors.END}\n")
        
        for i, dato in enumerate(self.buffer_recepcion):
            direccion = 0x2000 + i
            print(f"Dirección: 0x{direccion:04X}")
            print(f"  Contenido: '{dato['char']}' ({dato['binario']})")
            print(f"{Colors.CYAN}  10100010 {format(direccion & 0xFF, '08b')} {format((direccion >> 8) & 0xFF, '08b')}{Colors.END}")
            print(f"  → MOV [0x{direccion:04X}], AL  ; Guardar en memoria\n")
            time.sleep(0.8)
        
        print(f"{Colors.GREEN}✓ Datos almacenados en memoria RAM{Colors.END}")
        time.sleep(1)
    
    def escribir_archivo(self):
        """PASO 3: Escribir archivo en disco"""
        imprimir_titulo("COMPUTADORA RECEPTORA - PASO 3: Escritura en Disco")
        
        print(f"{Colors.YELLOW}💾 CREANDO ARCHIVO EN DISCO:{Colors.END}\n")
        
        instrucciones_escritura = [
            ("10110100 00111100", "MOV AH, 3Ch", "Función crear archivo"),
            ("10110001 00000000", "MOV CL, 0", "Atributos del archivo"),
            ("10001101 00011110", "LEA DX, [filename]", "Nombre del archivo"),
            ("11001101 00100001", "INT 21h", "Llamada al sistema - Crear"),
            ("10110100 01000000", "MOV AH, 40h", "Función escribir archivo"),
            ("10111001 00000001", "MOV CX, 1", "Escribir 1 byte"),
            ("11001101 00100001", "INT 21h", "Llamada al sistema - Escribir"),
            ("10110100 00111110", "MOV AH, 3Eh", "Función cerrar archivo"),
            ("11001101 00100001", "INT 21h", "Llamada al sistema - Cerrar"),
        ]
        
        for binario, asm, descripcion in instrucciones_escritura:
            print(f"{Colors.CYAN}{binario:30s}{Colors.END} → {asm:25s} ; {descripcion}")
            time.sleep(0.5)
        
        # Crear archivo real
        contenido = ''.join([dato['char'] for dato in self.buffer_recepcion])
        with open(self.archivo_destino, 'w') as f:
            f.write(contenido)
        
        print(f"\n{Colors.GREEN}✓ Archivo '{self.archivo_destino}' creado exitosamente{Colors.END}")
        print(f"{Colors.GREEN}✓ Contenido: '{contenido}'{Colors.END}")
        time.sleep(1)
    
    def verificar_integridad(self):
        """PASO 4: Verificar la integridad del archivo"""
        imprimir_titulo("COMPUTADORA RECEPTORA - PASO 4: Verificación")
        
        print(f"{Colors.YELLOW}🔍 VERIFICANDO INTEGRIDAD DEL ARCHIVO:{Colors.END}\n")
        
        with open(self.archivo_destino, 'r') as f:
            contenido = f.read()
        
        print(f"Archivo original:  'a'")
        print(f"Archivo recibido:  '{contenido}'")
        
        if contenido == 'a':
            print(f"\n{Colors.GREEN}✓✓✓ TRANSFERENCIA EXITOSA ✓✓✓{Colors.END}")
            print(f"{Colors.GREEN}Los archivos coinciden perfectamente{Colors.END}")
        else:
            print(f"\n{Colors.RED}✗ ERROR: Los archivos no coinciden{Colors.END}")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Función principal que coordina todo el proceso"""
    limpiar_pantalla()
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║         SIMULADOR DE TRANSFERENCIA USB A BAJO NIVEL              ║")
    print("║         Transferencia de archivo 'a' entre computadoras          ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Presiona ENTER para comenzar la simulación...{Colors.END}")
    
    # FASE 1: COMPUTADORA EMISORA
    print(f"\n\n{Colors.BOLD}{Colors.BLUE}{'*'*70}")
    print(f"{'FASE 1: COMPUTADORA EMISORA'.center(70)}")
    print(f"{'*'*70}{Colors.END}\n")
    time.sleep(1)
    
    emisor = ComputadoraEmisor()
    emisor.crear_archivo_origen()
    contenido = emisor.leer_archivo()
    emisor.cargar_en_memoria(contenido)
    emisor.preparar_transmision_usb()
    datos_transmitidos = emisor.transmitir_datos()
    
    # FASE 2: CANAL USB
    print(f"\n\n{Colors.BOLD}{Colors.BLUE}{'*'*70}")
    print(f"{'FASE 2: CANAL DE COMUNICACIÓN USB'.center(70)}")
    print(f"{'*'*70}{Colors.END}\n")
    time.sleep(1)
    
    canal = CanalUSB()
    datos_recibidos = canal.transmitir(datos_transmitidos)
    
    # FASE 3: COMPUTADORA RECEPTORA
    print(f"\n\n{Colors.BOLD}{Colors.BLUE}{'*'*70}")
    print(f"{'FASE 3: COMPUTADORA RECEPTORA'.center(70)}")
    print(f"{'*'*70}{Colors.END}\n")
    time.sleep(1)
    
    receptor = ComputadoraReceptor()
    receptor.recibir_datos_usb(datos_recibidos)
    receptor.almacenar_en_memoria()
    receptor.escribir_archivo()
    receptor.verificar_integridad()
    
    # RESUMEN FINAL
    imprimir_titulo("RESUMEN DE LA TRANSFERENCIA")
    
    print(f"{Colors.BOLD}Arquitectura del Sistema:{Colors.END}\n")
    print("┌─────────────────┐         ┌──────────┐         ┌─────────────────┐")
    print("│   COMPUTADORA   │         │  CABLE   │         │   COMPUTADORA   │")
    print("│     EMISORA     │ ══════▶ │   USB    │ ══════▶ │    RECEPTORA    │")
    print("└─────────────────┘         └──────────┘         └─────────────────┘")
    print("        │                                                 │")
    print("        ├─ CPU                                           ├─ CPU")
    print("        ├─ RAM                                           ├─ RAM")
    print("        ├─ Controlador USB                               ├─ Controlador USB")
    print("        └─ Sistema de Archivos                           └─ Sistema de Archivos")
    
    print(f"\n{Colors.BOLD}Estadísticas:{Colors.END}")
    print(f"  • Bytes transferidos: {len(datos_transmitidos)}")
    print(f"  • Protocolo: USB 2.0")
    print(f"  • Verificación: CRC")
    print(f"  • Estado: {Colors.GREEN}EXITOSO{Colors.END}")
    
    print(f"\n{Colors.BOLD}Archivos generados:{Colors.END}")
    print(f"  • Origen: archivo_a.txt")
    print(f"  • Destino: archivo_recibido.txt")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}¡SIMULACIÓN COMPLETADA!{Colors.END}\n")


if __name__ == "__main__":
    main()
