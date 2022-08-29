'use strict';

document.querySelectorAll(".delete_venue_btn").forEach(venue => {
    venue.addEventListener("click", (e) => {
    const venueID = e.target.dataset.id;
    // alert(venueID);
      // Update view
      e.target.parentElement.style.display = 'none';
      // Send request to controller then controller inform the Model for Update
      fetch(`/venues/${venueID}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(() => {

      })
      .catch(() => {

      });
    })
  });