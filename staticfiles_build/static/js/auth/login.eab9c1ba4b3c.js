const pwdInput = document.getElementById('password')
const showPwdBox = document.getElementById('pwd')
let pwdObscure = true

showPwdBox.addEventListener('click', () => {
  if (pwdObscure) {
    pwdInput.setAttribute('type', 'text')
    pwdObscure = false
  } else {
    pwdInput.setAttribute('type', 'password')
    pwdObscure = true
  }
})