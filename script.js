// Function to get nearby hospitals from backend
function getNearbyHospitals() {
    const location = document.getElementById('location').value;
    fetch(`/get_hospitals?location=${location}`)
        .then(response => response.json())
        .then(data => {
            let hospitalList = '<h2>Nearby Hospitals:</h2>';
            if (data.length === 0) {
                hospitalList += '<p>No hospitals found.</p>';
            } else {
                data.forEach(hospital => {
                    hospitalList += `<p><strong>${hospital.name}</strong><br>${hospital.address}</p>`;
                });
            }
            document.getElementById('hospital-list').innerHTML = hospitalList;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to get prevention advice from backend
function getPreventionAdvice() {
    const symptoms = document.getElementById('symptoms').value.split(',').map(symptom => symptom.trim());
    fetch('/get_advice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symptoms: symptoms })
    })
    .then(response => response.json())
    .then(data => {
        let adviceText = '<h2>Prevention Advice:</h2>';
        for (let symptom in data) {
            adviceText += `<p><strong>${symptom}:</strong> ${data[symptom]}</p>`;
        }
        document.getElementById('advice').innerHTML = adviceText;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
