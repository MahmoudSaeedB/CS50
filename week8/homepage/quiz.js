document.addEventListener('DOMContentLoaded', function()
{
    // Define a function that returns a random number withing a specific Range.
    function rand(min, max)
    {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    let firstNums = [];
    let secondNums = [];
    let products = [];
    let problems = document.querySelectorAll('.problem');
    let checks = document.querySelectorAll('.check');
    let answers = document.querySelectorAll('.answer');
    let feedbacks = document.querySelectorAll('.feedback');
    let grade = 0;
    let quizFinished = false;
    let checkCounts = 0;

    for (let i = 0; i < 7; i++)
    {
        firstNums[i] = rand(1, 12);
        secondNums[i] = rand(1,12);
        products[i] = firstNums[i] * secondNums[i];
        problems[i].innerHTML = `${firstNums[i]} &times ${secondNums[i]} = `;


        checks[i].onclick = function()
        {

            if (answers[i].value.trim() !== '')
            {
                checkCounts = i + 1;

                if (checkCounts === 7)
                {
                    quizFinished = true;
                }

                answers[i].disabled = true;
                checks[i].disabled = true;

                console.log(answers);
                console.log(products);
                if (answers[i].value.trim() == products[i])
                {
                    answers[i].style.backgroundColor = 'green';
                    feedbacks[i].innerHTML = 'Correct!'
                    grade++      
                }
                else
                {
                    answers[i].style.backgroundColor = 'red';
                    feedbacks[i].innerHTML = `Incorrect <br>${firstNums[i]} &times ${secondNums[i]} = ${products[i]}`
                } 
            }

        }
    }
    gradeButton.onclick = function()
    {
        if (quizFinished)
        {
            gradeButton.disabled = true;
            gradeMessage.innerHTML= `Your grade is ${grade}/7.`;
        }
    }
})