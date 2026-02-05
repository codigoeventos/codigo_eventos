"""
Utility functions for the Event Management System.
"""

import re
from datetime import datetime


def validate_cpf(cpf):
    """
    Validate Brazilian CPF number.
    
    Args:
        cpf: CPF string (can contain dots and dashes)
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove non-numeric characters
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Check if has 11 digits
    if len(cpf) != 11:
        return False
    
    # Check if all digits are the same
    if cpf == cpf[0] * 11:
        return False
    
    # Validate first check digit
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum_digits * 10 % 11) % 10
    
    if int(cpf[9]) != digit1:
        return False
    
    # Validate second check digit
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum_digits * 10 % 11) % 10
    
    if int(cpf[10]) != digit2:
        return False
    
    return True


def validate_cnpj(cnpj):
    """
    Validate Brazilian CNPJ number.
    
    Args:
        cnpj: CNPJ string (can contain dots, dashes, and slashes)
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove non-numeric characters
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Check if has 14 digits
    if len(cnpj) != 14:
        return False
    
    # Check if all digits are the same
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validate first check digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(12))
    digit1 = (sum_digits % 11)
    digit1 = 0 if digit1 < 2 else 11 - digit1
    
    if int(cnpj[12]) != digit1:
        return False
    
    # Validate second check digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(13))
    digit2 = (sum_digits % 11)
    digit2 = 0 if digit2 < 2 else 11 - digit2
    
    if int(cnpj[13]) != digit2:
        return False
    
    return True


def format_cpf(cpf):
    """Format CPF number with dots and dash."""
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def format_cnpj(cnpj):
    """Format CNPJ number with dots, slash, and dash."""
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj


def get_upload_path(instance, filename, subfolder=''):
    """
    Generate dynamic upload path for files.
    
    Args:
        instance: Model instance
        filename: Original filename
        subfolder: Optional subfolder name
        
    Returns:
        str: Upload path in format: app_name/model_name/id/subfolder/filename
    """
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Get the file extension
    ext = filename.split('.')[-1] if '.' in filename else ''
    base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
    
    # Clean filename
    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)
    new_filename = f"{clean_name}_{timestamp}.{ext}" if ext else f"{clean_name}_{timestamp}"
    
    if instance.pk:
        path = f"{app_name}/{model_name}/{instance.pk}"
    else:
        path = f"{app_name}/{model_name}/temp"
    
    if subfolder:
        path = f"{path}/{subfolder}"
    
    return f"{path}/{new_filename}"
