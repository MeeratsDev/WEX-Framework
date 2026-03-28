document.addEventListener('DOMContentLoaded', () => {
    const Navigation = {
        // Elements that can receive focus
        focusableSelector: 'a, button, input, [tabindex="0"]',

        // State
        lastFocusedElement: null,

        init() {
            // 1. Add keydown listener
            document.addEventListener('keydown', (e) => this.handleKeyDown(e));

            // 2. Add mouseover listener (optional: allows mouse to interact without breaking nav)
            document.addEventListener('mouseover', (e) => {
                const target = e.target.closest(this.focusableSelector);
                if (target && this.isVisible(target)) {
                    target.focus();
                }
            });

            // 3. Set initial focus
            this.focusFirstElement();
        },

        focusFirstElement() {
            // Priority: Active Popup -> Sidebar -> First Focusable
            const activePopup = document.querySelector('.popupPanel[style*="display: block"], .popupPanel.active');

            let scope = activePopup || document.body;
            const first = scope.querySelector(this.focusableSelector);
            if (first) {
                this.focus(first);
            }
        },

        handleKeyDown(e) {
            const current = document.activeElement;

            // Prevent default scrolling for arrow keys to let our logic handle it
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter"].includes(e.key)) {
                e.preventDefault();
            }

            switch (e.key) {
                case 'ArrowUp':
                    this.move('up');
                    break;
                case 'ArrowDown':
                    this.move('down');
                    break;
                case 'ArrowLeft':
                    this.move('left');
                    break;
                case 'ArrowRight':
                    this.move('right');
                    break;
                case 'Enter':
                    current.click();
                    break;
                case 'Escape':
                case 'Backspace':
                    // Logic to close popups if they are open
                    this.handleBack();
                    break;
            }
        },

        move(direction) {
            const current = document.activeElement;
            const activePopup = document.querySelector('.popupPanel[style*="display: block"], .popupPanel.active');

            // If a popup is open, restrict focus search to that popup
            const container = activePopup || document.body;

            // Get all focusable elements within the active context
            const allElements = Array.from(container.querySelectorAll(this.focusableSelector))
                                     .filter(el => this.isVisible(el));

            if (!allElements.length) return;

            const next = this.findNextElement(current, allElements, direction);

            if (next) {
                this.focus(next);
            }
        },

        findNextElement(current, candidates, direction) {
            const currentRect = current.getBoundingClientRect();
            let bestCandidate = null;
            let minDistance = Infinity;

            for (const candidate of candidates) {
                if (candidate === current) continue;

                const candidateRect = candidate.getBoundingClientRect();

                // 1. Directional Logic: Is the candidate actually in the direction we are going?
                if (!this.isInDirection(currentRect, candidateRect, direction)) continue;

                // 2. Distance Logic: Calculate Euclidean distance between centers
                const dist = this.getDistance(currentRect, candidateRect);

                // 3. Weighting: Prioritize alignment.
                // e.g. If moving UP, prioritize items directly above over items diagonally above.
                const alignment = this.getAlignment(currentRect, candidateRect, direction);

                // Combine distance and alignment (Weighted Distance)
                const weightedDist = dist + (alignment * 2);

                if (weightedDist < minDistance) {
                    minDistance = weightedDist;
                    bestCandidate = candidate;
                }
            }
            return bestCandidate;
        },

        // Check if candidate is strictly in the direction requested
        isInDirection(curr, cand, dir) {
            const cCenter = this.getCenter(curr);
            const candCenter = this.getCenter(cand);

            switch (dir) {
                case 'up': return candCenter.y < cCenter.y; // Candidate is above
                case 'down': return candCenter.y > cCenter.y; // Candidate is below
                case 'left': return candCenter.x < cCenter.x; // Candidate is left
                case 'right': return candCenter.x > cCenter.x; // Candidate is right
            }
            return false;
        },

        getCenter(rect) {
            return {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };
        },

        getDistance(r1, r2) {
            const c1 = this.getCenter(r1);
            const c2 = this.getCenter(r2);
            return Math.sqrt(Math.pow(c2.x - c1.x, 2) + Math.pow(c2.y - c1.y, 2));
        },

        // Calculate overlap offset to prioritize straight lines
        getAlignment(r1, r2, dir) {
            const c1 = this.getCenter(r1);
            const c2 = this.getCenter(r2);

            if (dir === 'left' || dir === 'right') {
                return Math.abs(c1.y - c2.y); // Vertical difference
            } else {
                return Math.abs(c1.x - c2.x); // Horizontal difference
            }
        },

        focus(element) {
            // Scroll logic: Center the element when focused
            element.focus();
            element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });

            // Add a focused class for CSS styling if needed
            // (Browser defaults usually handle Outline, but custom UI often needs this)
            document.querySelectorAll('.focused').forEach(el => el.classList.remove('focused'));
            element.classList.add('focused');
        },

        isVisible(el) {
            // Check if element handles visibility or is hidden by CSS
            if (el.offsetParent === null) return false;

            const style = window.getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;

            // Check if inside a generic hidden popup (if not the active one)
            const parentPopup = el.closest('.popupPanel');
            const activePopup = document.querySelector('.popupPanel[style*="display: block"], .popupPanel.active');

            if (parentPopup && parentPopup !== activePopup) return false;

            return true;
        },

        handleBack() {
            // Find open popups
            const openPopup = document.querySelector('.popupPanel[style*="display: block"], .popupPanel.active');

            if (openPopup) {
                // If using a close function from popup.js, trigger it.
                // Or simulate click on close button:
                const closeBtn = openPopup.querySelector('.closeButton'); // If exists
                if(closeBtn) closeBtn.click();

                // Or manually hide:
                openPopup.style.display = 'none';
                openPopup.classList.remove('active');

                // Refocus on main content (specifically the last focused item if possible)
                // For now, reset to Hero play button or Sidebar
                const fallback = document.querySelector('.hero .majorBtn') || document.querySelector('#sidebar a');
                if(fallback) this.focus(fallback);
            }
        }
    };

    Navigation.init();
});
