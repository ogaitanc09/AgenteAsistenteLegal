import sys
print("Python usado:", sys.executable)

try:
    import dotenv
    from dotenv import load_dotenv
    print("IMPORT CORRECTO: dotenv funciona")
except Exception as e:
    print("ERROR IMPORTANDO dotenv:", e)
