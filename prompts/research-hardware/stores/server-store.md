# The Server Store

Apply [the shared listing contract](../listings.md). Discover public product links through
<https://www.theserverstore.com/product_index.asp>, then open preconfigured systems matching the query.

Read “Total price”, part number, Availability and the preconfigured description. Optional configuration controls can
change RAM, processors or storage; a base price does not establish the price of an upgraded selection. “GPU capable”
does not mean GPUs are included. Reject barebones and systems without included CPUs/RAM from CPU-system candidates.
Extract installed DIMM count and speed only when stated; the platform's slot count and maximum speed are not enough
to calculate the delivered server's bandwidth.

Explicit “Out of Stock. 0” overrides a readable price, pickup text and generic purchase controls. Several tested
preconfigured listings had this status. Return them in `rejected`, then continue to other stores if no eligible
inventory is found. Return the shared result; do not mistake the extended-warranty price for the server price.
