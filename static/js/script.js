/**************--------Pulse Animation Effect Start--------**************/
document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.pulse');
  
  buttons.forEach(button => {
      button.addEventListener('click', function() {
          button.classList.add('animate');
          setTimeout(() => button.classList.remove('animate'), 500); 
      });
  });
});
/**************--------Pulse Animation Effect End--------**************/