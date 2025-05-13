document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const clearButton = document.getElementById('clearButton');
    const correctInputs = document.querySelectorAll('#correctLetters input');
    const misplacedInputs = document.querySelectorAll('#misplacedLetters input');
    const excludedInput = document.getElementById('excludedLetters');

    const letterInputs = document.querySelectorAll('input[type="text"]');
    letterInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase().replace(/[^A-Z]/g, '');
        });
    });

    clearButton.addEventListener('click', function() {
        correctInputs.forEach(input => input.value = '');
        misplacedInputs.forEach(input => input.value = '');
        excludedInput.value = '';
        
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.style.display = 'none';
        resultsContainer.innerHTML = '';
    });

    searchButton.addEventListener('click', async function() {
        const correctLetters = Array.from(correctInputs).map(input => ({
            letter: input.value.toLowerCase(),
            position: Array.from(correctInputs).indexOf(input)
        })).filter(item => item.letter !== '');

        const misplacedLetters = Array.from(misplacedInputs).map(input => ({
            letter: input.value.toLowerCase(),
            position: Array.from(misplacedInputs).indexOf(input)
        })).filter(item => item.letter !== '');

        const excludedLetters = excludedInput.value.toLowerCase().split('');

        const response = await fetch('/api/find', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correctLetters,
                misplacedLetters,
                excludedLetters
            })
        });

        const data = await response.json();
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.style.display = 'block';
        
        if (data.words && data.words.length > 0) {
            resultsContainer.innerHTML = '<h3>Word Tuah Possible Answers:</h3>' +
                data.words.map(word => `<span class="word-chip">${word}</span>`).join('');
        } else {
            resultsContainer.innerHTML = '<p>No matching words found for Word Tuah</p>';
        }
    });
});
