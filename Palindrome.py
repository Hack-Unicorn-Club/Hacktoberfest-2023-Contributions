#Python program to check string is Palindrome or not 

st = input("Enter a String: ")

if st == st[::-1]:
    print("String is palidrome")
else:
    print("string is not Palidrome")    
    