import pytest
from server import app


def tester():
    app.config["TESTING"] = True
    with app.test_client() as tester:
        print('=> *** I am a fixture : WebApp was successfully created and the test was : ')
        yield tester




# test unitaire pour s'assurer que le serveur se lance correctement
def test_lance_correct():
    tester=app.test_client()
    response =tester.get('/')
    assert response.status_code == 200


#  test unitaire pour s'assurer qu'un summary est affiché
def test_showSummary_valid_mail():
    tester=app.test_client()
    r = tester.post("/showSummary" , data ={"email":"admin@irontemple.com"}, follow_redirects=True)
    r.status_code==200
    data = r.data.decode()
    assert "wlecome"

 # test unitaire pour s'assurer qu'un message d'erreur est affiché lorsque le mail est incorrect
def test_showSummary_invalid_mail():
    tester =app.test_client()
    r = tester.post("/showSummary" , data ={"email":"gggg@gmail.com"}, follow_redirects=True)
    r.status_code == 200
    data= r.data.decode()
    assert 'Desole , cet email n a pas ete trouve' in data

# test unitaire pour s'assurer qu'il affiche une page booking.html pour un club ou une competition
def test_book_valid_compet_club():
    tester = app.test_client()
    url ="http://127.0.0.1:5000/book/Spring%20Festival/Iron%20Temple"
    r= tester.get(url) 
    r.status_code ==200 
    data = r.data.decode()
    print(data)
      
    
# test unitaire pour s'assurer que l'interface utilisateur empeche la reservation d'un club ou competition non valide
def test_book_invalid_compet_club():
    tester = app.test_client()
    url ="http://127.0.0.1:5000/book/fake_compet/fake_club"
    r = tester.get(url, follow_redirects=True) 
    r.status_code ==200 
    data = r.data.decode()
    print(data)  

#test unitaire pour s'assurer que les place sont correctement déduites lors d'un achat
def test_valid():
    tester=app.test_client()
    r = tester.post("/purchasePlaces" , data =dict(club="Iron Temple",competition="Spring Festival", places="3"), follow_redirects=True)

    data = r.data.decode()
    assert "Number of Places: 0" in data
    assert "Points available: 1" in data
    

#test unitaire pour s'assurer qu'un message d'erreur est afficher lorsqu'on achete plus de place que de points disponibles
def test_innvalid():
    tester=app.test_client()
    r = tester.post("/purchasePlaces" , data =dict(club="Iron Temple",competition="Spring Festival", places="5"), follow_redirects=True)

    data = r.data.decode()
    assert "desole nous n avons pas assez de places" in data
    print(data)   

#test unitaire pour s'assurer qu'un message d'erreur est afficher lorsqu'on achete plus de 12 places
def test_innnvalid():
    tester=app.test_client()
    r = tester.post("/purchasePlaces" , data =dict(club="Iron Temple",competition="Fall Classic", places="13"), follow_redirects=True)

    data = r.data.decode()
    assert "desole vous ne pouvez pas reserver au delas de 12 places" in data
    print(data)      
 



#test unitaire pour logout   
def test_logout():
    tester =app.test_client()
    r=tester.get('/logout', follow_redirects=True)
    assert r.status_code == 200


    
    

    

    
