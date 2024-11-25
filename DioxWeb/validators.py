# archivo: myapp/validators.py

import re
from django.core.exceptions import ValidationError

def validar_rut(rut):
    """
    Función para validar el RUT chileno.
    Verifica el formato y calcula el dígito verificador.
    """
    # Eliminar puntos y guion
    rut = rut.replace('.', '').replace('-', '')

    # Verificar que el RUT tenga el formato adecuado
    if not re.match(r'^[0-9]{7,8}[0-9Kk]{1}$', rut):
        raise ValidationError("RUT inválido. El formato debe ser 12345678-9 o 12345678-K.")

    # Extraer el número y el dígito verificador
    rut_num = rut[:-1]
    dv = rut[-1].upper()

    # Calcular el dígito verificador
    suma = 0
    multiplo = 2
    for i in reversed(rut_num):
        suma += int(i) * multiplo
        multiplo = 9 if multiplo == 2 else multiplo + 1

    resto = suma % 11
    dv_calculado = str(11 - resto) if resto != 1 else 'K'
    dv_calculado = '0' if resto == 0 else dv_calculado

    # Verificar si el dígito verificador coincide
    if dv != dv_calculado:
        raise ValidationError("RUT inválido. El dígito verificador no es correcto.")
    
    return rut
