/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2023 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
    'use strict'

    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)

    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme()
        if (storedTheme) {
            return storedTheme
        }

        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }

    const setTheme = theme => {
        if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark')
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme)
        }
    }

    setTheme(getPreferredTheme())

    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector('#bd-theme')

        if (!themeSwitcher) {
            return
        }

        const themeSwitcherText = document.querySelector('#bd-theme-text')
        const activeThemeIcon = document.querySelector('.theme-icon-active use')
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
        const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')

        document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
        })

        btnToActive.classList.add('active')
        btnToActive.setAttribute('aria-pressed', 'true')
        activeThemeIcon.setAttribute('href', svgOfActiveBtn)
        const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`
        themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)

        if (focus) {
            themeSwitcher.focus()
        }
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        const storedTheme = getStoredTheme()
        if (storedTheme !== 'light' && storedTheme !== 'dark') {
            setTheme(getPreferredTheme())
        }
    })

    window.addEventListener('DOMContentLoaded', () => {
        const themeSwitch = document.querySelector('#bd-theme')

        themeSwitch.checked = getPreferredTheme() === 'dark'
        themeSwitch.addEventListener('change', () => {
            const theme = themeSwitch.checked ? 'dark' : 'light';
            setStoredTheme(theme);
            setTheme(theme);
            showActiveTheme(theme, true);
        })
    })
})
()

// Обрамляет теги img в тег a добавляя к изображению класс img-fluid
// window.onload = function () {
//     var paragraphs = document.querySelectorAll('p img');
//     for (var i = 0; i < paragraphs.length; i++) {
//         var image = paragraphs[i];
//         var imageUrl = image.getAttribute('src');
//
//         // Добавляем класс img-fluid к изображению
//         image.classList.add('img-fluid');
//
//         // Создаем новый элемент <a>
//         var link = document.createElement('a');
//         link.href = imageUrl;
//         link.setAttribute('data-lightbox', 'image-1');
//
//         // Заменяем изображение ссылкой
//         image.parentNode.replaceChild(link, image);
//         link.appendChild(image);
//     }
// };
//
// window.onload = function() {
//     var codeElements = document.getElementsByTagName('code');
//     for(var i = 0; i < codeElements.length; i++) {
//         codeElements[i].setAttribute('id', 'to-copy' + i);
//
//         codeElements[i].addEventListener('click', function() {
//             var range = document.createRange();
//             range.selectNode(this);
//             window.getSelection().removeAllRanges();
//             window.getSelection().addRange(range);
//             document.execCommand('copy');
//             window.getSelection().removeAllRanges();
//             // alert('Скопировано в буфер обмена!');
//         });
//     }
// };

window.onload = function () {
    let i;
    const paragraphs = document.querySelectorAll('figure img');
    for (i = 0; i < paragraphs.length; i++) {
        const image = paragraphs[i];
        const imageUrl = image.getAttribute('src');

        // Добавляем класс img-fluid к изображению
        image.classList.add('img-fluid');

        // Создаем новый элемент <a>
        const link = document.createElement('a');
        link.href = imageUrl;
        link.setAttribute('data-lightbox', 'image-1');

        // Заменяем изображение ссылкой
        image.parentNode.replaceChild(link, image);
        link.appendChild(image);
    }

const codeElements = document.getElementsByTagName('code');
for(i = 0; i < codeElements.length; i++) {
    codeElements[i].setAttribute('id', 'to-copy' + i);

    codeElements[i].addEventListener('click', function() {
        const range = document.createRange();
        range.selectNode(this);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();

        const tooltip = document.createElement('div');
        tooltip.textContent = 'Текст скопирован!';
        tooltip.style.position = 'fixed';
        tooltip.style.background = '#000';
        tooltip.style.color = '#fff';
        tooltip.style.padding = '10px';
        tooltip.style.borderRadius = '5px';
        tooltip.style.left = (event.clientX + 10) + 'px';
        tooltip.style.top = (event.clientY + 10) + 'px';
        document.body.appendChild(tooltip);

        setTimeout(function() {
            tooltip.remove();
        }, 2000);
    });
}
};