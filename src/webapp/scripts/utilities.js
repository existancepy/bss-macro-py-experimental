/*
=============================================
Misc
=============================================
*/
//javascript function to capitalize the first letter of a string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

//javascript function to convert a string to title case
function toTitleCase(str) {
    return str.replace(
      /\w\S*/g,
      text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
    );
}

/*
=============================================
UI
=============================================
*/
const saveGeneralTriggerFunction = "saveSetting(this, 'general')"
const saveProfileTriggerFunction = "saveSetting(this, 'profile')"