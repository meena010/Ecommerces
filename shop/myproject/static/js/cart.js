console.log("Hello,World")
window.onload = function() {
var buttons = document.querySelectorAll('.update-cart');
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
    var coffeeId = this.dataset.coffeeId
    var action = this.dataset.action
    console.log('coffeeId:', coffeeId, 'action:', action) 

    console.log('USER:', user)
    if( user == 'AnonymousUser'){
        console.log('User is not authenticated')
    }else{
        updateUserOrder(coffeeId, action)
    }
});
}
function updateUserOrder(coffeeId, action){
    console.log('User is authenticated, ending data...')

     var url= '/update_item/'
     console.log('url:', url)

     fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body:JSON.stringify({'coffeeId': coffeeId, 'action': action})
     })
     .then((response)=>{
        return response.json();
     })
     .then((data)=>{
        location.reload()
     })
}
}