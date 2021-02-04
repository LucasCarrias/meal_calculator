# Meal Calculator :bacon:

Calculadora de valor de refeição

---

## Requisitos e Instalação
Você precisa do Python 3.8 :snake: ou superior instalado para executar os scripts

### Dependências
Para instalação das dependências você precisa executar o seguinte comando:
```
pipenv install
```
Para ativação do ambiente virtual:
```
pipenv shell
```

## Executar o serividor

```
python manage.py runserver 8000
```
Você pode acessar todos os endpoints em:
**/api-docs/swagger**

## Testes
Tests foram criados para todos os endpoints e algumas regras de validação. Para rodar:
```
python manage.py test
```

## Models

Models utilizados para a aplicação:

![Models](https://github.com/LucasCarrias/meal_calculator/blob/main/.docs/models.png)
