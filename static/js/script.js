/**************--------Pulse Animation Effect Start--------**************/
document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.pulse');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      button.classList.add('animate');
      setTimeout(() => button.classList.remove('animate'), 500);
    });
  });
});
/**************--------Pulse Animation Effect End--------**************/

/**************--------Video Thumbnail Start--------**************/
document.addEventListener('DOMContentLoaded', function () {
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
});
/**************--------Video Thumbnail End--------**************/
