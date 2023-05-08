document.addEventListener('DOMContentLoaded', () => {
  // ! cart
  const cartBtn = document.querySelector('#cart-btn')
  const cartWrapper = document.querySelector('#cart-wrapper')
  const cartCloseBtn = document.querySelector('#cart-close-btn')
  const overlayElement = document.createElement('div')
  overlayElement.classList.add('overlay')

  cartBtn.addEventListener('click', () => {
    cartWrapper.classList.add('show')
  })
  cartCloseBtn.addEventListener('click', () => {
    cartWrapper.classList.remove('show')
  })
  overlayElement.onclick = () => {
    cartWrapper.classList.remove('show')
  }
  cartWrapper.addEventListener('transitionend', () => {
    if (cartWrapper.classList.contains('show')) {
      document.body.append(overlayElement)
      document.body.style.overflow = 'hidden'
    } else {
      overlayElement.remove()
      document.body.style.overflow = ''
    }
  })
})
