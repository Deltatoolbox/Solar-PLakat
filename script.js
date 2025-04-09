document.addEventListener('DOMContentLoaded', () => {
    const advantages = document.querySelectorAll('.advantage');
    const solarPanel = document.querySelector('.solar-panel');
    const sun = document.querySelector('.sun');
    const moon = document.querySelector('.moon');
    const batteryLevel = document.querySelector('.battery-level');
    const houseLight = document.querySelector('.light');
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    // Make sun draggable
    sun.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === sun) {
            isDragging = true;
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, sun);
        }
    }

    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    // Add parallax effect to moon
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        moon.style.transform = `translate(${x * -20}px, ${y * -20}px)`;
    });

    // Add hover effect to solar panel
    solarPanel.addEventListener('mouseenter', () => {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.style.animation = 'shine 1s infinite';
        });
        // Charge battery when hovering over solar panel
        batteryLevel.style.height = '100%';
        // Light up the house
        houseLight.style.backgroundColor = 'rgba(255, 255, 0, 0.8)';
    });

    solarPanel.addEventListener('mouseleave', () => {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.style.animation = 'shine 3s infinite';
        });
        // Discharge battery when leaving solar panel
        batteryLevel.style.height = '0%';
        // Turn off the house light
        houseLight.style.backgroundColor = 'rgba(255, 255, 0, 0)';
    });

    // Add hover effect to advantages
    advantages.forEach(advantage => {
        advantage.addEventListener('mouseenter', () => {
            advantage.style.transform = 'translateY(-10px)';
        });

        advantage.addEventListener('mouseleave', () => {
            advantage.style.transform = 'translateY(0)';
        });
    });

    // Add scroll animation
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        solarPanel.style.transform = `perspective(1000px) rotateX(${20 + scrollPosition * 0.02}deg)`;
    });
}); 