# self.driver.get('https://www.ricardo.ch/de/s/')
#
#         # Using readlines()
#         file1 = open('UpperCategories.txt', 'r')
#         Lines = file1.readlines()
#
#         links = []
#
#         count = 0
#         # Strips the newline character
#         for line in Lines:
#             self.driver.get(line.strip())
#
#             lnks = self.driver.find_elements_by_tag_name("a")
#             # traverse list
#             for lnk in lnks:
#                 # get_attribute() to get all href
#                 if '/c/' in str(lnk.get_attribute("href")) and '/de/' in str(
#                         lnk.get_attribute("href")) and "page" not in str(lnk.get_attribute("href")) and not str(
#                     lnk.get_attribute("href")) == line:
#
#                     # print(lnk.get_attribute("href"))
#                     links.append(str(lnk.get_attribute("href")))
#                     # print('count', links.count(lnk.get_attribute("href")), '\n')
#                     # if (links.count(lnk.get_attribute("href")) == 3):
#                     #     print(lnk.get_attribute("href"))
#
#         for link in links:
#             if (links.count(link) == 1):
#                 print(link)
#
#         for link in links:
#             if (links.count(link) <3):
#                 print(links.count(link))