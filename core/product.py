class Product:
    def __init__(
        self,
        name="N/A",
        original_price="N/A",
        discounted_price="N/A",
        monthly_payment="N/A",
        url="N/A",
    ):
        self.name = name
        self.original_price = original_price
        self.discounted_price = discounted_price
        self.monthly_payment = monthly_payment
        self.url = url

    def to_dict(self):
        return {
            "name": self.name,
            "original_price": self.original_price,
            "discounted_price": self.discounted_price,
            "monthly_payment": self.monthly_payment,
            "url": self.url,
        }

    def __str__(self):
        return f"{self.name} | Original: {self.original_price} | Discounted: {self.discounted_price}"
