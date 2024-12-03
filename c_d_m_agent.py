from C_D_M import C_D_M_funcations as cdm
product="Ansys Startup Program is designed to support early-stage startups by providing them with access to Ansys' industry-leading simulation software at discounted prices. This program helps startups tackle engineering challenges more affordably and efficiently, reducing the need for physical prototyping and accelerating time to market. "

#suggesting icp for our product
icp=cdm.ideal_customer_profile(product)
data=open("icp.txt","w")
data.write(str(icp))
data.close()


#suggesting icp for our product
personas=cdm.create_profile(icp)
data=open("personas.txt","w")
data.write(str(personas))
data.close()

#asking qestions to persona
qestions=["Does this product solve your issue?","Is this a good product?""How frequently do you purchase this product?","How many percent of users purchase repeatedly?","Is this product recommendable?","What is the overall customer review or feedback from product reviewers?","Can the product be improved according to product reviews?","How many of the adopters are still using the product?","What are the chances a customer is disappointed with the product?","What is the general rating of the product?"]
data=open("questions.txt","w")
for persona in personas:
    if len(persona)>=10:
        data.write(str(persona)+"\n")
        answers=cdm.qestions_for_personas(qestions,persona,product)
        data.write(str(answers))
    else:
        pass
data.close()
