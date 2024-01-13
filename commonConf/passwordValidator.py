def password_check(passwd):
    SpecialSym =['$', '@', '#', '%']
    contaxt = {
            'status':True,
            'message':"password is valid"
            }
    if len(passwd) < 6:
        contaxt = {
            'status':False,
            'message':'length should be at least 6'
            }
        return contaxt
 
    if len(passwd) > 20:
        contaxt = {
            'status':False,
            'message':'length should be not be greater than 8'
            }
        return contaxt
 
    # Check if password contains at least one digit, uppercase letter, lowercase letter, and special symbol
    has_digit = False
    has_upper = False
    has_lower = False
    has_sym = False
    for char in passwd:
        if ord(char) >= 48 and ord(char) <= 57:
            has_digit = True
        elif ord(char) >= 65 and ord(char) <= 90:
            has_upper = True
        elif ord(char) >= 97 and ord(char) <= 122:
            has_lower = True
        elif char in SpecialSym:
            has_sym = True
 
    if not has_digit:
        contaxt = {
            'status':False,
            'message':'Password should have at least one numeral'
            }
        return contaxt
    if not has_upper:
        contaxt = {
            'status':False,
            'message':'Password should have at least one uppercase letter'
            }
        return contaxt
    if not has_lower:
        contaxt = {
            'status':False,
            'message':'Password should have at least one lowercase letter'
            }
        return contaxt
    if not has_sym:
        contaxt = {
            'status':False,
            'message':'Password should have at least one of the symbols $@#'
            }
        return contaxt
    if contaxt['status']:
        return contaxt