"""
TEST FILE TO IMPLEMENT A GRPAH TO SEARCH DATA about a user question
"""

"""
Tree Structure:

    The knowledge tree will have a hierarchical structure to accommodate various topics and conversations.
    The top-level nodes will represent general categories such as Friends, Family, Work, Fun, etc.
    Under each general category, there will be nodes representing specific organizations or entities, such as School, Company, Organization, etc.
    Within each organization or entity, there will be nodes representing specific topics like Studies, Entrepreneurship, Sports, etc.
    Finally, under each topic, the core elements of conversations and their associated data will be stored.
"""

# CREATE A GRAPH out of a json file PER user to help Ao to retrieve data
{
    "category": {
        "organizations": {
            "topics": {
                "core_element_conv": {

                }
            }
        }
    }
}