/**
 * Railway Reservation System - Client-side Interaction
 */

document.addEventListener('DOMContentLoaded', () => {
    // Station Swap Button in Search Form
    const swapBtn = document.getElementById('btn-swap-stations');
    if (swapBtn) {
        swapBtn.addEventListener('click', () => {
            const originSelect = document.getElementById('origin');
            const destSelect = document.getElementById('destination');
            if (originSelect && destSelect) {
                const temp = originSelect.value;
                originSelect.value = destSelect.value;
                destSelect.value = temp;
            }
        });
    }

    // Dynamic Seat Selection based on Class selection in Booking Form
    const runIdInput = document.getElementById('book-run-id');
    const classSelect = document.getElementById('book-class-select');
    const seatSelect = document.getElementById('book-seat-select');
    const originInput = document.getElementById('book-origin-id');
    const destInput = document.getElementById('book-dest-id');

    function refreshSeats() {
        if (!runIdInput || !classSelect || !seatSelect || !originInput || !destInput) return;
        const runId = runIdInput.value;
        const travelClass = classSelect.value;
        const originId = originInput.value;
        const destId = destInput.value;

        if (!runId || !travelClass || !originId || !destId) return;

        seatSelect.innerHTML = '<option value="">Loading available seats...</option>';

        fetch(`/api/available-seats?run_id=${runId}&travel_class=${encodeURIComponent(travelClass)}&origin_id=${originId}&dest_id=${destId}`)
            .then(res => res.json())
            .then(data => {
                seatSelect.innerHTML = '<option value="">-- Auto-Allocate Optimal Berth --</option>';
                if (data.seats && data.seats.length > 0) {
                    data.seats.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.seat_id;
                        opt.textContent = `Seat ${s.coach_code}-${s.seat_number} (${s.berth_type})`;
                        seatSelect.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement('option');
                    opt.value = "";
                    opt.textContent = "No confirmed seats (Will place on Waitlist)";
                    seatSelect.appendChild(opt);
                }
            })
            .catch(err => {
                console.error("Error fetching available seats:", err);
                seatSelect.innerHTML = '<option value="">Auto-Allocate</option>';
            });
    }

    if (classSelect) {
        classSelect.addEventListener('change', refreshSeats);
    }
});
