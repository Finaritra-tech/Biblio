const boutons = document.querySelectorAll('.ouvrirPopup');
const overlay = document.getElementById('popupOverlay');
const fermer = document.getElementById('fermerPopup');
const nomInput = document.getElementById('nomInput');
const livreIdInput = document.getElementById('livreIdInput');
const formPopup = document.getElementById('formPopup');


  boutons.forEach(bouton => {
    bouton.addEventListener('click', () => {


      const nom = bouton.getAttribute('data-nom');
      const livreId = bouton.getAttribute('data-id');
      nomInput.innerHTML = nom; 
      livreIdInput.value = livreId;
      formPopup.action = `/ajouter_panier/${livreId}/`;
      overlay.style.display = 'flex';
    });
  });

 
  fermer.addEventListener('click', () => {
    overlay.style.display = 'none';
  });

 
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.style.display = 'none';
    }
  });