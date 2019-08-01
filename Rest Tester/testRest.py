import json
import requests

# First request to determine expected values
request = "https://reqres.in/api/users?page=1"
response = requests.get(request)
json_data = json.loads(response.text)
responseFirstData = json_data
expectedPageCount = json_data['total_pages']
expectedUsersPerPage = json_data['per_page']
expectedTotalUserCount = json_data['total']
pageCount = expectedPageCount
usersPerPage = expectedUsersPerPage
totalUserCount = expectedUsersPerPage
expId = 1
expFName = "George"
expLName = "Bluth"
expEmail = "george.bluth@reqres.in"
expAvatar = "https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg"

# Other requests to calculate values
for iterator in range(2, expectedPageCount+1):
    request = "https://reqres.in/api/users?page=" + str(iterator)
    response = requests.get(request)
    json_data = json.loads(response.text)
    pageCount = iterator
    usersPerPage = len(json_data['data'])
    totalUserCount += usersPerPage

# Print result of task 1
print("Task 1")
print("Number of pages: ", pageCount, end="")
if pageCount == expectedPageCount:
    print(", as expected.")
else:
    print(", but expected amount was: ", expectedPageCount)

print("Number of users per page: ", usersPerPage, end="")
if usersPerPage == expectedUsersPerPage:
    print(", as expected.")
else:
    print(", but expected amount was: ", expectedUsersPerPage)

print("Total number of users: ", totalUserCount, end="")
if totalUserCount == expectedTotalUserCount:
    print(", as expected.")
else:
    print(", but expected amount was: ", expectedTotalUserCount)

# Print result of task 2
print("\nTask 2")
# Check top level fields
if ('page' in responseFirstData and 'per_page' in responseFirstData
        and 'total' in responseFirstData and 'total_pages' in responseFirstData
        and 'data' in responseFirstData):
    print("All fields are present")
else:
    print("page "*('page' not in responseFirstData),
          "per_page "*('per_page' not in responseFirstData),
          "total "*('total' not in responseFirstData),
          "total_pages "*('total_pages' not in responseFirstData),
          "data "*('data' not in responseFirstData), "are not present")
data = responseFirstData['data']
# Check data field


if len(data) != 0:
    allFields = (('id' in data[0]) and ('email' in data[0]) and ('first_name' in data[0]) and
                 ('last_name' in data[0]) and ('avatar' in data[0]))
    if allFields:
        print("All fields in data are present")
        # Print result of task 3
        print("\nTask 3")
        # Validate data field for id = 0 from the first page
        userValidate = ((data[0]['id'] == expId) and (data[0]['email'] == expEmail) and
                        (data[0]['first_name'] == expFName) and (data[0]['last_name'] == expLName) and
                        (data[0]['avatar'] == expAvatar))
        if userValidate:
            print("User validated")
        else:
            print("The following data doesnt match expected values: ",
                  "id " * (data[0]['id'] != expId),
                  "email " * (data[0]['email'] != expEmail),
                  "first_name " * (data[0]['first_name'] != expFName),
                  "last_name " * (data[0]['last_name'] != expLName),
                  "avatar " * (data[0]['avatar'] != expAvatar))
    else:
        print("id " * ('id' not in data[0]),
              "email " * ('email' not in data[0]),
              "first_name " * ('first_name' not in data[0]),
              "last_name " * ('last_name' not in data[0]),
              "avatar " * ('avatar' not in data[0]), "are not present\nTask 3 result is False as well")
else:
    print("Data field is empty\nTask 3 result is False as well")
