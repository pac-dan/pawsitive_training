/**
 * Video.js player initialization for training videos
 */
document.addEventListener('DOMContentLoaded', function() {
    var videoElement = document.getElementById('my-video');
    
    if (videoElement) {
        var player = videojs('my-video', {
            fluid: true,
            responsive: true,
            playbackRates: [0.5, 1, 1.25, 1.5, 2],
            controlBar: {
                volumePanel: {
                    inline: false
                }
            }
        });

        // Handle errors
        player.on('error', function() {
            var error = player.error();
            console.error('Video.js error:', error);
        });

        // Log when video is ready
        player.on('ready', function() {
            console.log('Video player is ready');
        });
    }
});

