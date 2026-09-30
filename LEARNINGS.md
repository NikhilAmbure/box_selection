# From this assignment I've learned about following things:

1) 3D packing Algorithm : It the biggest thing that i learned throughout the project building,
   Learned about how to physically fit the products into the boxes via calculating the volumes, 
    dimensions, weight and all. Initially, i was trying to solve it by greedy method, but there were
    a lot of calculation needed for the project like i have to calculate the free space available 
    after one product put into the box and then there were 3 more scenarios where i have to consider
    about how much space will be there left above the product, beside the product and box space left,
    so, i have to split the space into three different regions.
    And also there was a scenario of rotation that's the most challenging one for me to understand the whole
    permutations we needed for product's dimensions.

2) dataclasses : I never used it or heard about it. So, while getting suggestions from ai i got this 
    new concept and learned about it too what it is , how it works. How frozen = True make them immutable.
    Instead of going through the django models database layer it allowed me to keep packing logic independent.