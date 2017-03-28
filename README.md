
# Num2Geo
Num2Geo არის django Template tag რომელიც გვაძლევს საშუალებას 1.000.000-მდე ნებისმიერი რიცხვი გადავთარგმნოთ, მივუწეროთ ნებისმიერი ვალუტა და გამოვყოთ რიცხვი მძიმეებით.

##გამოყენების ინსტრუქცია
ricxvebi.py ფაილს ვაგდებთ templatetags-ში და შემდეგ django template-ში გადასათარგმნელ ცვლადს ვუწერთ შემდეგნაირად {{ ricxvi|num2geo:'შესაბამისი პარამეტრი' }}.

## მაგალითები

#### template:
```
{% load ricxvebi %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p>{{ ricxvi }}</p>
<p>{{ ricxvi|num2geo:'number_with_translate' }}</p>
</body>
</html>
```

#### view:
```
def demo(request):
    ricxvi = 500000
    return TemplateResponse(request, 'demo.html', {'ricxvi': ricxvi})
```

#### აბრუნებს:
500000

500,000.00 (ხუთასი ათასი და 0.00)

### requirements
ჯერჯერობით django 1.8 და python 2.7