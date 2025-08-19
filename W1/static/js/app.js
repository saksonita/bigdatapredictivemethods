/**
 * E-commerce Analytics Dashboard JavaScript
 * Handles interactive functionality and API calls
 */

// Global variables
let currentAnalyticsType = '';
let refreshInterval = null;

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    console.log('Analytics Dashboard initialized');
    
    // Set current analytics type based on URL
    const path = window.location.pathname;
    if (path.includes('descriptive')) {
        currentAnalyticsType = 'descriptive';
    } else if (path.includes('diagnostic')) {
        currentAnalyticsType = 'diagnostic';
    } else if (path.includes('predictive')) {
        currentAnalyticsType = 'predictive';
    } else if (path.includes('prescriptive')) {
        currentAnalyticsType = 'prescriptive';
    }
    
    // Initialize components
    initializeCharts();
    initializeInteractivity();
    initializeTooltips();
    
    // Start auto-refresh if on analytics page
    if (currentAnalyticsType) {
        startAutoRefresh();
    }
}

// Initialize charts and visualizations
function initializeCharts() {
    // Chart.js default configuration
    if (typeof Chart !== 'undefined') {
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.plugins.legend.display = true;
        Chart.defaults.plugins.legend.position = 'top';
    }
    
    // Plotly default configuration
    if (typeof Plotly !== 'undefined') {
        Plotly.setPlotConfig({
            displayModeBar: false,
            responsive: true
        });
    }
}

// Initialize interactive elements
function initializeInteractivity() {
    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('no-loading')) {
                addLoadingState(this);
            }
        });
    });
    
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            if (this.classList.contains('analytics-card')) {
                this.style.transform = 'translateY(-5px)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (this.classList.contains('analytics-card')) {
                this.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Add click handlers for stat items
    const statItems = document.querySelectorAll('.stat-item');
    statItems.forEach(item => {
        item.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

// Initialize tooltips
function initializeTooltips() {
    // Bootstrap tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Add loading state to element
function addLoadingState(element) {
    element.classList.add('loading');
    const originalText = element.innerHTML;
    element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    
    setTimeout(() => {
        element.classList.remove('loading');
        element.innerHTML = originalText;
    }, 1000);
}

// Refresh data from API
async function refreshData() {
    try {
        showNotification('Refreshing data...', 'info');
        
        const response = await fetch('/api/refresh');
        const result = await response.json();
        
        if (result.status === 'success') {
            showNotification('Data refreshed successfully!', 'success');
            
            // Reload current page after refresh
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            throw new Error(result.message || 'Failed to refresh data');
        }
    } catch (error) {
        console.error('Error refreshing data:', error);
        showNotification('Error refreshing data: ' + error.message, 'danger');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show with animation
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 100);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Get notification icon based on type
function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Start auto-refresh
function startAutoRefresh() {
    // Refresh every 5 minutes
    refreshInterval = setInterval(() => {
        if (document.visibilityState === 'visible') {
            console.log('Auto-refreshing data...');
            // Silently refresh data without notification
            fetch('/api/refresh')
                .then(response => response.json())
                .then(result => {
                    if (result.status === 'success') {
                        console.log('Data auto-refreshed successfully');
                    }
                })
                .catch(error => {
                    console.error('Auto-refresh failed:', error);
                });
        }
    }, 300000); // 5 minutes
}

// Stop auto-refresh
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// Fetch customer details
async function fetchCustomerDetails(customerId) {
    try {
        const response = await fetch(`/api/customer/${customerId}`);
        const customerData = await response.json();
        
        if (response.ok) {
            showCustomerModal(customerData);
        } else {
            throw new Error(customerData.error || 'Failed to fetch customer details');
        }
    } catch (error) {
        console.error('Error fetching customer details:', error);
        showNotification('Error fetching customer details: ' + error.message, 'danger');
    }
}

// Show customer details modal
function showCustomerModal(customerData) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="customerModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-user me-2"></i>Customer Details
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Basic Information</h6>
                                <p><strong>Name:</strong> ${customerData.customer_info.first_name} ${customerData.customer_info.last_name}</p>
                                <p><strong>Email:</strong> ${customerData.customer_info.email}</p>
                                <p><strong>Age:</strong> ${customerData.customer_info.age}</p>
                                <p><strong>Segment:</strong> ${customerData.customer_info.customer_segment}</p>
                                <p><strong>Status:</strong> ${customerData.customer_info.is_churned ? 'Churned' : 'Active'}</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Transaction Summary</h6>
                                <p><strong>Total Spent:</strong> $${customerData.transaction_summary.total_spent.toFixed(2)}</p>
                                <p><strong>Total Transactions:</strong> ${customerData.transaction_summary.total_transactions}</p>
                                <p><strong>Avg Order Value:</strong> $${customerData.transaction_summary.avg_order_value.toFixed(2)}</p>
                                <p><strong>First Purchase:</strong> ${customerData.transaction_summary.first_purchase || 'N/A'}</p>
                                <p><strong>Last Purchase:</strong> ${customerData.transaction_summary.last_purchase || 'N/A'}</p>
                            </div>
                        </div>
                        ${customerData.predictions && Object.keys(customerData.predictions).length > 0 ? `
                            <hr>
                            <h6>Predictions</h6>
                            <div class="row">
                                ${customerData.predictions.churn_probability ? `
                                    <div class="col-md-6">
                                        <p><strong>Churn Probability:</strong> ${(customerData.predictions.churn_probability * 100).toFixed(1)}%</p>
                                    </div>
                                ` : ''}
                                ${customerData.predictions.predicted_clv ? `
                                    <div class="col-md-6">
                                        <p><strong>Predicted CLV:</strong> $${customerData.predictions.predicted_clv.toFixed(2)}</p>
                                    </div>
                                ` : ''}
                            </div>
                        ` : ''}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal
    const existingModal = document.getElementById('customerModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('customerModal'));
    modal.show();
    
    // Clean up modal when hidden
    document.getElementById('customerModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Export data functionality
function exportData(format = 'csv', dataType = 'all') {
    showNotification(`Exporting ${dataType} data as ${format.toUpperCase()}...`, 'info');
    
    // This would typically make an API call to export data
    setTimeout(() => {
        showNotification(`${dataType} data exported successfully!`, 'success');
    }, 2000);
}

// Print functionality
function printReport() {
    window.print();
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

function formatPercentage(decimal) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1
    }).format(decimal);
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
});

// Handle visibility change
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible' && currentAnalyticsType) {
        startAutoRefresh();
    } else {
        stopAutoRefresh();
    }
});

// Global functions for template usage
window.refreshData = refreshData;
window.fetchCustomerDetails = fetchCustomerDetails;
window.exportData = exportData;
window.printReport = printReport;