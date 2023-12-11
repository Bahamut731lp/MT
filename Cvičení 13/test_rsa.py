from my_rsa import rsa

is_successfull = True

for i in range(100):
    result = rsa("ahoj")

    if result["original"]["numerical"] != result["decyphered"]["numerical"]:
        print(result["original"]["numerical"], result["decyphered"]["numerical"])
        is_successfull = False
        break

if is_successfull:
    print("All runs were successfull")
else:
    print("There was an error")