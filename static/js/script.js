document.addEventListener('DOMContentLoaded', function () {
    /**************--------Sort & Filter Function Start--------**************/
    const filterOptions = document.getElementById('filter-options');

    filterOptions.addEventListener('change', function () {
        const selectedCourseId = this.value;
        const items = document.querySelectorAll('.library-item');

        items.forEach(item => {
            const itemCourseId = item.getAttribute('data-course-id');

            if (selectedCourseId === 'all' || itemCourseId === selectedCourseId) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });

    const sortOptions = document.getElementById('sort-options');

    sortOptions.addEventListener('change', function () {
        const sortValue = this.value;
        const itemsContainer = document.querySelector('.module-list, .video-list, .course-list');
        const items = Array.from(itemsContainer.children);

        items.sort((a, b) => {
            if (sortValue === 'title') {
                return a.querySelector('.card-title').innerText.localeCompare(b.querySelector('.card-title').innerText);
            } else if (sortValue === 'date') {
                return new Date(a.getAttribute('data-date')) - new Date(b.getAttribute('data-date'));
            }
        });

        items.forEach(item => itemsContainer.appendChild(item));
    });

    /**************--------Sort & Filter Function End--------**************/

    /**************--------Pulse Animation Effect Start--------**************/
    const buttons = document.querySelectorAll('.pulse');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            button.classList.add('animate');
            setTimeout(() => button.classList.remove('animate'), 500);
        });
    });
    /**************--------Pulse Animation Effect End--------**************/

    // External video play
    const videoThumbnails = document.querySelectorAll('.video-thumbnail');

    videoThumbnails.forEach(thumbnail => {
        const playButton = thumbnail.querySelector('.play-button');
        playButton.addEventListener('click', function () {
            const videoId = thumbnail.getAttribute('data-video-id');
            const videoContainer = document.getElementById(`video-container-${videoId}`);

            if (videoContainer.innerHTML === '') {
                const iframe = document.createElement('iframe');
                iframe.width = '560';
                iframe.height = '315';
                iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
                iframe.frameBorder = '0';
                iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
                iframe.allowFullscreen = true;

                videoContainer.innerHTML = '';
                videoContainer.appendChild(iframe);
            }

            videoContainer.querySelector('iframe').style.display = 'block';
        });
    });

    /**************--------Add User Click Start--------**************/
    // const courseItems = document.querySelectorAll('.library-item');

    // courseItems.forEach(item => {
    //     item.addEventListener('dblclick', function () {
    //         const description = this.querySelector('.card-text');
    //         if (description) {
    //             description.style.display = (description.style.display === 'none' || description.style.display === '') ? 'block' : 'none';
    //         }
    //     });
    // });
    // document.addEventListener('DOMContentLoaded', () => {
        // const courseItems = document.querySelectorAll('.library-item');
    
        // courseItems.forEach(item => {
        //     item.addEventListener('dblclick', function () {
        //         const shortDesc = this.querySelector('.short-desc');
        //         const fullDesc = this.querySelector('.full-desc');
        //         if (fullDesc.style.display === 'none' || fullDesc.style.display === '') {
        //             fullDesc.style.display = 'block';
        //             shortDesc.style.display = 'none';
        //         } else {
        //             fullDesc.style.display = 'none';
        //             shortDesc.style.display = 'block';
        //         }
        //     });
        // });
    // });
 // ----------------------------------Last updated code Select all description containers
 // Select all thumbnail images
 const thumbnails = document.querySelectorAll('.card-img-top');

 // Function to toggle between short and full descriptions
 function toggleDescription(event) {
     const cardBody = event.currentTarget.closest('.library-item').querySelector('.card-body');
     const shortDesc = cardBody.querySelector('.short-desc');
     const fullDesc = cardBody.querySelector('.full-desc');

     if (fullDesc.style.display === 'none') {
         fullDesc.style.display = 'block';
         shortDesc.style.display = 'none';
     } else {
         fullDesc.style.display = 'none';
         shortDesc.style.display = 'block';
     }
 }

 // Attach double-click event listener to each thumbnail
 thumbnails.forEach(thumbnail => {
     thumbnail.addEventListener('dblclick', toggleDescription);
 });
    
    /**************--------Add User Click End--------**************/
});