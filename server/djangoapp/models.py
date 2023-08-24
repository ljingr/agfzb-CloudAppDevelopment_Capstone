from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=30)

    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(null=False,max_length=30)
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealer_id = models.CharField(null=False,max_length=60)
    TYPE_CHOICES = (("SED","Sedan"), ("SUV","SUV"), ("WAG","WAGON"),("etc","etc."))
    car_type = models.CharField(max_length=9,choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return "Name:" + self.name + "," + \
            "Car Make:" + self.car_make + "," + \
                "Dealer id:" + self.dealer_id + "," + \
                    "Type:"+ self.car_type + "," + \
                        "year:" + + self.year



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
