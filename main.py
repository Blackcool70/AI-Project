
from classifier import *

# london = Entity("London")
# people["London"] = london
# user_likes_restaurant(london, "taco bell", priority=7)
# user_likes_restaurant(london, "burger king", priority=10)
# user_likes_restaurant(london, "mcdonalds", priority=10)
# user_likes_restaurant(london, "wendys", priority=8)
# user_likes_restaurant(london, "whataburger", priority=4)
# user_likes_restaurant(london, "abuelos", priority=3)
# user_likes_restaurant(london, "best thai restaurant", priority=2)
# user_likes_restaurant(london, "rosas")
# user_likes_restaurant(london, "roadhouse")
# print_top_N("London", 25)
# print("\n"*2)
#
# ##############################################
#
# rachel = Entity("Rachel")
# people["Rachel"] = rachel
#
# user_likes_restaurant(rachel, "taco bell", priority=10)
# user_likes_restaurant(rachel, "rosas", priority=10)
# user_likes_restaurant(rachel, "burger king", priority=15)
# user_likes_restaurant(rachel, "whataburger", priority=1)
# user_likes_restaurant(rachel, "buffalo wild wings", priority=9)
# user_likes_restaurant(rachel, "roadhouse", priority=5)
# user_likes_restaurant(rachel, "pizza hut", priority=10)
# print_top_N("Rachel", 25)
# print("\n"*2)
#
# ##############################################
# atef = Entity("Atef")
# people["Atef"] = atef
# user_likes_restaurant(atef, "taco bell", priority=3)
# user_likes_restaurant(atef, "burger king", priority=15)
# user_likes_restaurant(atef, "mcdonalds", priority=15)
# user_likes_restaurant(atef, "braums", priority=12)
# user_likes_restaurant(atef, "subway", priority=6)
# user_likes_restaurant(atef, "chik-fil-a", priority=7)
# user_likes_restaurant(atef, "dominos", priority=7)
# user_likes_restaurant(atef, "best thai restaurant", priority=7)
# print_top_N("Atef", 15)
# print("\n"*2)
#
# ##############################################
# jecsan = Entity("Jecsan")
# people["Jecsan"] = jecsan
# user_likes_restaurant(jecsan, "burger king", priority=10)
# user_likes_restaurant(jecsan, "mcdonalds", priority=5)
# user_likes_restaurant(jecsan, "buffalo wild wings", priority=2)
# print_top_N("Jecsan", 15)
# print("\n"*2)
#
# ##############################################
#
# print(find_group_top_N_restaurants([london, rachel, atef, jecsan], 5))


APP_NAME = "APP.ETITE"


class Restaurant:
    def __init__(self, name, priority=1):
        self.name = name
        self.priority = priority

    def get_name(self):
        return self.name

    def get_priority(self):
        return self.priority

    def __str__(self):
        return f"{self.name}"

    def __getitem__(self,index):
        return self.name[index]

    def __setitem__(self,index,value):
        self.name[index] = value

class Member:
    def __init__(self, name):
        self.name = name
        self.liked_restaurants = []

    def likes(self, restaurant):
        self.liked_restaurants.append(restaurant)

    def get_liked_restaurants(self):
        return self.liked_restaurants

    def __iter__(self):
        return iter(self.get_liked_restaurants())

    def __getitem__(self,index):
        return self.liked_restaurants[index]

    def __setitem__(self,index,value):
        self.liked_restaurants[index] = value
    def __str__(self):
        return self.name


class Group:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def add_member(self, member):
        self.members.append(member)

    def get_members(self):
        return self.members

    def get_name(self):
        return self.name

    def __str__(self):
        return f"Name: {self.name}"

    def __len__(self):
        return len(self.members)


def format_members_to_str(values):
    string = ""
    for value in values:
        string.join(str(value).join(","))
    return string


def create_members(member_name_list):
    members = []
    for name in member_name_list:
        members.append(Member(name))
    return members


def csv2list(csv, sep=','):
    lst = list(map(lambda s: s.strip(), csv.split(sep)))
    if len(lst) == 1 and lst[0] == '': return []
    return lst

def main():
    print()
    print(f"{APP_NAME}")
    print()
    try:
        fp = open('data.txt')
        lines = fp.readlines()
        group_name = lines[0]
        print(f"Group name: {group_name.capitalize()}")
        member_names = csv2list(lines[1])
        print("Group member's names:")
        for i,n in enumerate(member_names,start=1):
            print(f"{i}. {n}")
        print()
        group = Group(group_name, create_members(member_names))
        for i,member in enumerate(group.get_members(),start=2):
            if i>=len(lines):break
            restaurants = csv2list(lines[i])
            for restaurant in restaurants:
                restaurant = Restaurant(csv2list(restaurant, sep=':'))
                member.likes(restaurant)
    finally:
        fp.close()

    members = []
    for member in group.get_members():
        m = Entity(member)
        members.append(m)
        people[member] = m
        for likes in member.get_liked_restaurants():
            r = likes[0]
            p = int(likes[1])
            user_likes_restaurant(m,r,p)
        print_top_N(member,5)
        print("\n"*2)

    print(f"After a lot of thought, I have decided that the group should go eat at: [{find_group_top_N_restaurants(members,1)[0]}]")

if __name__ == '__main__':
    main()
