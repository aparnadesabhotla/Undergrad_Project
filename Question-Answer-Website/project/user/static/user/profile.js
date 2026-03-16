const showUpdateProfileFormButton = document.querySelector('#show-update-profile-form-button');
const hideUpdateProfileFormButton = document.querySelector('#hide-update-profile-form-button')
const updateProfileForm = document.querySelector('#update-profile-form');

loadEventListeners();

function loadEventListeners()
{
    showUpdateProfileFormButton.addEventListener('click', showUpdateProfileForm);
    hideUpdateProfileFormButton.addEventListener('click', hideUpdateProfileForm);
}

function showUpdateProfileForm()
{
    showUpdateProfileFormButton.style.display = 'none';
    updateProfileForm.style.display = 'block';
}

function hideUpdateProfileForm()
{
    showUpdateProfileFormButton.style.display = 'block';
    updateProfileForm.style.display = 'none';
}