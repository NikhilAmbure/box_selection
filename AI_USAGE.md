# AI_USAGE.md

## AI tools that i used

1) Claude (claude.ai) :

## Prompts

1) prompt: "I received this assignment. As per my understanding, i have to build an ai assisted box selection system where i have to map the order details of the order that user placed, then the order goes to warehouse where all the products are stored, then i have to find that which shipping box to use according to the weight/dimensions of the parcel/product that user ordered, and there are several types of boxes with different dimensions and weight capacity with it's cost. So, i would need order details model which contains the product with foreign key field, quantity, created_at field , and then product model which contains the product_id, product_weight, dimensions of the product, cost of the product and i will need the one method in order details which will calculate the total cost, total weight of ordered products, highest dimension between ordered products, and the third model will be shipping box there will be name field, weight of the box, cost of the box, dimension of the box. For now this will be the architecture. Next what algorithms do u suggest to get those products fit into it. As i researched about it i have once solved one leetcode problem based on some minimum cost candies something problem where i used greedy algorithm. Do i need greedy algo here too?? Or is there any other algorithm so solve this problem??"
    why : "Here, i wanted to give a brief about what i understood about the assignment, if i was wrong about the architecture then 
    It should have pointed it out to recheck the architecture decision. And also discussed about which algorithm should i use 
    to implement in this project which will solve the problem for me."
2) prompt : "Yesterday , I read about the algorithm a guillotine 3D packing heuristic. when i recieved this assignment. so basically it works like by my understanding: we have to calculate the free spaces in the box in three different scenarios firstly we have to place one product lets say A (10x10x10) cm , B(20x10x5) and then C(15x8x8) cm and Box : 40x20x20 cm. Actaully i will attach my notes that i made while learning it check it out. And i think this algo will work in this assignment."
    why : the day i received the assignment i firstly approached it with the white paper and pen by myself, evaluated
    the problem on paper and tried to solve it firstly and with the help of google i researched about some algorithm to use
    and got the guilloto's 3d packing algorithm, i understood that problem with the example and wrote it down.
    here, i am verifying and asked claude to implement the algorithm for me later.
3) prompt : "also how can i implement the rotation logic here??"
    why : Rotation logic for the products to fit in the box, some products needed to rotation so they can
    fit in the different regions which are available in the spaces list in the project.
4) prompt : "Also i would remove those co-ordinates and up-right rotation part, How can some human calculate those exact placement co-ordinates by this its just everyone has their own iq so depends"
    prompt : "also u added box_weight field in dataclass Box but we have given the box_weight_capacity already. It is mentioned in the assignment"
    prompt: "As i can see your implementation i think we dont need to add those multiple boxes concept here bc in assignment we just have to select a box for the specific order so i will remove those unnecessary functions."
    
    why : They are three different prompts that i gave to claude to remove the implemented algorithm that he gave
    i wanted him to remove those co-ordinates and up-right rotation, explicitly defined box_weight( which is already given by the problem)
    and at last that multiple boxes implementation from the algorithm i removed these because here we have to only choose 
    one box selection and also problem statement didnt mentioned about selecting the multiple boxes, for coordinates its not 
    possible for a human/worker to fit exactly calculated dimensions of products as it is, but for robots it will work
    so i removed it from the project.
5) prompt : "instead of drf can we design it in django?? views.py dont use serializers"
    why : I later changed the views implementation from drf to plain django, because of standard django
    views with JsonResponse would be sufficient for handling requests and responses without adding the 
    serializer layer. And it was the simple approach for me.

## Output i accepted

1) Project Architecture : I accepted the architecture that claude gave me just made changes into the fields 
    which will look good for me (like naming the fields)
2) 3D packing algorithm : Based on my notes i decided to implement this algorithm with the help of claude,
3) I accepted the use of standard Django views and `JsonResponse` instead of Django REST Framework serializers.

## Output I rejected or modified

1) Multi-box split removed  beacuse the assignment only asked for the one box per order
2) co-ordinates and upright rotation : removed 
3) DRF views and serializers
4) Product ids in requests -> changed it with product names
5) 
## AI Mistakes Identified

1) The AI introduced additional features such as multi-box packing,
placement coordinates, and upright rotation constraints that were not required by the assignment.
I reviewed the requirements and removed them to 
keep the implementation focused on the requested box-selection problem.

## How I verified the final code

1) I tested it manually via postman
2) Verified the output for the algorithm via hand written notes 