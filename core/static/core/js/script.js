// Row slider controls
document.addEventListener('DOMContentLoaded', function () {
    const leftBtns = document.querySelectorAll('.left-btn');
    const rightBtns = document.querySelectorAll('.right-btn');
  
    leftBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.target);
        target.scrollBy({ left: -260, behavior: 'smooth' });
      });
    });
    rightBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.target);
        target.scrollBy({ left: 260, behavior: 'smooth' });
      });
    });
  
    // Drag to scroll
    const sliders = document.querySelectorAll('.row-slider');
    sliders.forEach(slider => {
      let isDown = false, startX, scrollLeft;
      slider.addEventListener('mousedown', (e) => {
        isDown = true;
        slider.classList.add('active');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
      });
      slider.addEventListener('mouseleave', () => { isDown = false; slider.classList.remove('active'); });
      slider.addEventListener('mouseup', () => { isDown = false; slider.classList.remove('active'); });
      slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1; //scroll-fast
        slider.scrollLeft = scrollLeft - walk;
      });
    });
  });