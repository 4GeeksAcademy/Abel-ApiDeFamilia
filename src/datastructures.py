"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list

requirments:
  -  All requests and responses should be in content/type: application/json
  -  Response codes must be 200 for success, 400 for bad request, or 404 for not found.
  -  These exercises do not include a database, everything must be done in Runtime (RAM).
"""


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }

        ]

    # This method generates a unique incremental ID
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        member["id"] = self._generate_id()
        member["last_name"] = self.last_name
        self._members.append(member)
        return self.get_member(member["id"])

    def delete_member(self, id):
        member = self.get_member(id)
        if not member:
            return False
        self._members.remove(member)
        return True

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
