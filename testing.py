from C_D_M import C_D_M_funcations as cdm
product="Ansys Startup Program is designed to support early-stage startups by providing them with access to Ansys' industry-leading simulation software at discounted prices. This program helps startups tackle engineering challenges more affordably and efficiently, reducing the need for physical prototyping and accelerating time to market. "
icp=cdm.ideal_customer_profile(product)
icp = cdm.structure_icp_data(icp)
print(icp)