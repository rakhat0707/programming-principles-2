import re

print("1. 'a' followed by zero or more 'b'")
pattern1 = r"^ab*$"
print(bool(re.match(pattern1, "a")))
print(bool(re.match(pattern1, "ab")))
print(bool(re.match(pattern1, "abbbb")))
print()

print("2. 'a' followed by two to three 'b'")
pattern2 = r"^ab{2,3}$"
print(bool(re.match(pattern2, "abb")))
print(bool(re.match(pattern2, "abbb")))
print()

print("3. lowercase letters joined with underscore")
pattern3 = r"\b[a-z]+_[a-z]+\b"
text3 = "hello_world test_value OK"
print(re.findall(pattern3, text3))
print()

print("4. One uppercase followed by lowercase letters")
pattern4 = r"\b[A-Z][a-z]+\b"
text4 = "Hello World test Example"
print(re.findall(pattern4, text4))
print()

print("5. 'a' followed by anything ending in 'b'")
pattern5 = r"^a.*b$"
print(bool(re.match(pattern5, "axxxb")))
print()

print("6. Replace space, comma, dot with colon")
text6 = "Hello, world. Test string"
print(re.sub(r"[ ,\.]", ":", text6))
print()

print("7. snake_case to camelCase")
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))
print()

print("8. Split at uppercase letters")
text8 = "HelloWorldTest"
print(re.split(r"(?=[A-Z])", text8))
print()

print("9. Insert spaces before capital letters")
text9 = "HelloWorldTest"
print(re.sub(r"(?<!^)(?=[A-Z])", " ", text9))
print()

print("10. camelCase to snake_case")
def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(camel_to_snake("HelloWorldTest"))