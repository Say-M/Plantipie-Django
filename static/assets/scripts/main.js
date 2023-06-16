document.addEventListener('DOMContentLoaded', () => {
  // ! cart
  const cart_aside = new URLSearchParams(window.location.search).get(
    'cart_aside'
  )
  const cartBtn = document.querySelector('#cart-btn')
  const cartWrapper = document.querySelector('#cart-wrapper')
  const cartCloseBtn = document.querySelector('#cart-close-btn')
  const overlayElement = document.createElement('div')
  overlayElement.classList.add('overlay')

  if (cart_aside) {
    cartWrapper.classList.add('show')
    document.body.append(overlayElement)
    document.body.style.overflow = 'hidden'
  }

  cartBtn.addEventListener('click', () => {
    cartWrapper.classList.add('show')
    document.body.append(overlayElement)
    document.body.style.overflow = 'hidden'
  })
  cartCloseBtn.addEventListener('click', () => {
    cartWrapper.classList.remove('show')
    overlayElement.remove()
    document.body.style.overflow = ''
  })
  overlayElement.onclick = () => {
    cartWrapper.classList.remove('show')
    overlayElement.remove()
    document.body.style.overflow = ''
  }
  // cartWrapper.addEventListener('transitionend', () => {
  //   if (cartWrapper.classList.contains('show')) {
  //     document.body.append(overlayElement)
  //     document.body.style.overflow = 'hidden'
  //   } else {
  //     overlayElement.remove()
  //     document.body.style.overflow = ''
  //   }
  // })
})
