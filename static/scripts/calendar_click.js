document.addEventListener('DOMContentLoaded', function() {
    function handleDayClick(event) {
        const clickedDay = event.target;
        // Check if clicked element is a day (a TD element with a number)
        if (clickedDay.tagName === "TD" && !isNaN(clickedDay.innerText) && clickedDay.innerText !== '') {
            clickedDay.classList.add('day-clicked');

            fetch(`/calendar_day/${clickedDay.innerText}`)
                .then(response => response.json())
                .then(data => {
                    let output = '<ul>';

                    let dayList = data.data;

                    for (let item of dayList) {
                        output += `<li>${item}</li>`;
                    }
                    output += '</ul>';  // Close the unordered list

                    document.getElementById('dictData').innerHTML = output;
                })
        }
    }

    // Add the click event listener to the table
    const calendarTable = document.querySelector('.calendar');
    calendarTable.addEventListener('click', handleDayClick);
});