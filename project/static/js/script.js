document.addEventListener('DOMContentLoaded', function() {
    const message = document.getElementById('message');
    const showMessageBtn = document.getElementById('showMessageBtn');
    let clickCount = 0;
    let isMessageVisible = false;

    const soundAppear = document.getElementById('soundAppear');
    const soundDisappear = document.getElementById('soundDisappear');
    const soundLeveledUp = document.getElementById('soundLeveledUp');
    const soundGlitch = new Audio('soundGlitch.mp3');

    soundLeveledUp.volume = 0.2;

    let messages = [
        `<p>Ты же уже видел сегодняшние достижения?!</p> 
         <p>У тебя проблемы с реакцией или памятью?</p> 
         <p>Явно не мои проблемы, решай их сам...</p> 
         <p>Что за невнимательность? Теперь с тобой не разговариваю!</p>`
    ];

    function showGlitchText(element, text, delay = 50) {
        let chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
        let glitchText = text.split("").map(() => chars[Math.floor(Math.random() * chars.length)]).join("");
        element.textContent = glitchText;
        let i = 0;
        let interval = setInterval(() => {
            if (i >= text.length) {
                clearInterval(interval);
            } else {
                glitchText = glitchText.substring(0, i) + text[i] + glitchText.substring(i + 1);
                element.textContent = glitchText;
                i++;
            }
        }, delay);
    }

    function showMessage() {
        clickCount++;

        if (clickCount === 1) {
            message.style.display = 'block';
            message.style.animation = 'showMessage 1s forwards';
            soundAppear.play();
            isMessageVisible = true;
        } else if (clickCount === 2) {
            message.innerHTML = messageText;
            message.style.display = 'block';
            message.style.animation = 'showMessage 1s forwards';
            soundLeveledUp.play();
            isMessageVisible = true;
        } else if (clickCount === 3) {
            showMessageBtn.disabled = true;
            showGlitchText(showMessageBtn, "??????????????????");
            setTimeout(() => showGlitchText(showMessageBtn, "Я предупреждал..."), 3000);

            message.innerHTML = `<p id="glitchMessage"></p>`;
            showGlitchText(document.getElementById("glitchMessage"), "ТЫ НАПРОСИЛСЯ...", 100);
            message.style.display = 'block';
            message.style.animation = 'showMessage 1s forwards';
            soundGlitch.play();
            isMessageVisible = true;
        }
    }

    function hideMessage() {
        if (isMessageVisible) {
            message.style.animation = 'disappearEffect 1s forwards';
            soundDisappear.play();
            setTimeout(() => {
                message.style.display = 'none';
                isMessageVisible = false;
            }, 1000);
        }
    }

    showMessageBtn.addEventListener('click', showMessage);
    message.addEventListener('click', hideMessage);

    const waterLevel = document.getElementById('waterLevel');
    const drinkWaterBtn = document.getElementById('drinkWaterBtn');
    let waterPercentage = 0;
    const maxWater = 100;
    const glassSize = 17;

    function createBubble() {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.style.width = `${Math.random() * 10 + 5}px`;
        bubble.style.height = bubble.style.width;
        bubble.style.left = `${Math.random() * 80}%`;
        bubble.style.animationDuration = `${Math.random() * 2 + 1.5}s`;

        waterLevel.appendChild(bubble);
        setTimeout(() => bubble.remove(), 3000);
    }

    function showWaterMessage() {
        message.innerHTML = `
            <div class="flex">
                <div class="tittle-notification">
                    <div class="circle">!</div>
                </div>
                <div><h3>NOTIFICATION</h3></div>
            </div>
            <p>А ты не лопнешь?</p>
            <p class="level">На сегодня хватит воды!</p>
        `;

        message.style.display = 'block';
        message.style.animation = 'showMessage 1s forwards';
        soundLeveledUp.play();
        isMessageVisible = true;
    }

    drinkWaterBtn.addEventListener('click', function() {
        if (waterPercentage < maxWater) {
            waterPercentage += glassSize;
            waterLevel.style.height = waterPercentage + '%';
            createBubble();
        }

        if (waterPercentage >= maxWater) {
            showWaterMessage();
        }
    });
    document.addEventListener('DOMContentLoaded', function() {
    const waterLevel = document.getElementById('waterLevel');
        const drinkWaterBtn = document.getElementById('drinkWaterBtn');
        let waterPercentage = 0;
        const maxWater = 100;
        const glassSize = 20;

        drinkWaterBtn.addEventListener('click', function() {
            if (waterPercentage < maxWater) {
                waterPercentage += glassSize;
                waterLevel.style.height = waterPercentage + '%';
            }

            if (waterPercentage >= maxWater) {
                message.style.display = 'block';
                drinkWaterBtn.disabled = true;
            }
        });
    });
});
