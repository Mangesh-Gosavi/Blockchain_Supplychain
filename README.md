In this blockchain-based supply chain system developed using Flask, the primary objective is to create a secure and transparent record of products as they move through the supply chain. Employees and administrators are granted the ability to input product information into the system, including crucial details such as product name and description. However, the process of initiating the creation of a new block, which essentially represents a product in the blockchain, is reserved for administrators. When a product block is "mined" by an admin, it incorporates the product details and the hash of the previous block, ensuring a chain-like structure. Once a block is created, it becomes visible to all participants involved in the supply chain, promoting transparency and accountability.

Additionally, various stakeholders in the supply chain, such as raw suppliers, manufacturers, suppliers, and retailers, are allowed to update the status of products as they progress along the chain. This could include status updates like "sent","received". As products move through different stages, their statuses are updated accordingly, providing a comprehensive view of their journey.

To enhance tracking and monitoring, a "tracker" feature is implemented, offering a comprehensive overview of a product's journey through the supply chain. This tracker consolidates all the status updates and relevant information associated with the product, allowing stakeholders to easily trace its path from raw materials to the end consumer. The implementation encapsulates user authentication to distinguish between various roles in the supply chain, ensuring the appropriate access and actions for employees, administrators, suppliers, and retailers. Through this system, the blockchain acts as an immutable ledger, enhancing trust and visibility within the supply chain ecosystem.

rawmaterial: https://blockchain-supplychain.vercel.app/rawmat
manufacturer: https://blockchain-supplychain.vercel.app/manufac
supplier: https://blockchain-supplychain.vercel.app/supplier
retailer: https://blockchain-supplychain.vercel.app/retailer

