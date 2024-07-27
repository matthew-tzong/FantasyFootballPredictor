import React, { useState, useEffect } from 'react';
import axios from 'axios';
// Import CSS File & Images for Header
import './PlayerStats.css';
import leftImage from './Lamar-Jackson-PNG-Clipart.png';
import rightImage from './PatrickMahomesClipArt.avif';

// 30 records per page
const PAGE_SIZE = 30; 

//State variable to manage component state
const PlayerStats = () => {
    const [stats, setStats] = useState([]);  //Player Stats
    const [loading, setLoading] = useState(true); //Track loading status
    const [error, setError] = useState(null); //Store errors
    const [view, setView] = useState('PPR'); // Track which view is selected (PPR/NonPPR)
    const [sortColumn, setSortColumn] = useState('Fantasy PPR Points'); //Column to sort data by initially
    const [sortDirection, setSortDirection] = useState('desc'); 
    const [searchTerm, setSearchTerm] = useState(''); // Search term for filtering players
    const [currentPage, setCurrentPage] = useState(1); // Current page
    const [selectedPlayers, setSelectedPlayers] = useState([]); // Track selected players for team

    //Get player statistics from from API whenever view changes, sort it
    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/statistics');
                const sortedData = sortData(response.data, sortColumn, sortDirection);
                setStats(sortedData);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            }
        };

        fetchStats();
    }, [sortColumn, sortDirection, view]);

    //Format statistics to 3 decimal values or 0.000 for null values
    const formatNumber = (number) => {
        if (number === null) {
            return '0.000'; 
        }
        return number.toFixed(3);
    };

    //Handle different view depending on PPR/NonPPR button
    const handleViewChange = (newView) => {
        setView(newView);
        setSortColumn(newView === 'PPR' ? 'Fantasy PPR Points' : 'Fantasy Non-PPR Points');
    };

    //Handle sorting by specific columns
    const handleSort = (column) => {
        const newDirection = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
        setSortColumn(column);
        setSortDirection(newDirection);
    };

    //Sort Data for given Column/Direction
    const sortData = (data, column, direction) => {
        return [...data].sort((a, b) => {
            const valueA = a[column] || 0;
            const valueB = b[column] || 0;
            if (direction === 'asc') {
                return valueA - valueB;
            } else {
                return valueB - valueA;
            }
        });
    };

    //Get player based on search filter
    const filteredStats = stats.filter(stat => 
        stat.Player.toLowerCase().includes(searchTerm.toLowerCase())
    );

    //Paginate after search filter
    const paginatedStats = filteredStats.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);
    const totalPages = Math.ceil(filteredStats.length / PAGE_SIZE);

    //Handle page changes
    const handlePageChange = (page) => {
        if (page > 0 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

    //Shows if data is sorted in ascending or descending order
    const getSortClass = (column) => {
        if (sortColumn === column) {
            return sortDirection === 'asc' ? 'sort-asc' : 'sort-desc';
        }
        return '';
    };

    //Handle selecting/deselecting a player for a team
    const handleSelectPlayer = (player) => {
        setSelectedPlayers((prevSelected) => {
            if (prevSelected.includes(player)) {
                return prevSelected.filter(p => p !== player);
            } else {
                return [...prevSelected, player];
            }
        });
    };

    //Reset Team
    const handleResetTeam = () => {
        setSelectedPlayers([]);
    };

    //Calculate total projected points for chosen team
    const totalPoints = selectedPlayers.reduce((total, player) => {
        const playerData = stats.find(stat => stat.Player === player);
        if (playerData) {
            return total + (view === 'PPR' ? playerData['Fantasy PPR Points'] : playerData['Fantasy Non-PPR Points']);
        }
        return total;
    }, 0);

    //Render loading/error page
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error fetching data: {error.message}</p>;


    //Return rendered components
    return (
        <div className="container">
            <header className="header">
                <img src= {leftImage} alt="Left Banner" className="header-image left" />
                <h1>Fantasy Football Stat Predictor</h1>
                <img src= {rightImage} alt="Right Banner" className="header-image right" />
            </header>
            <div className="toggle-button">
                <button 
                    onClick={() => handleViewChange('PPR')}
                    className={view === 'PPR' ? 'button-active' : 'button-inactive'}
                >
                    PPR
                </button>
                <button 
                    onClick={() => handleViewChange('Non-PPR')}
                    className={view === 'Non-PPR' ? 'button-active' : 'button-inactive'}
                >
                    Non-PPR
                </button>
            </div>
            <div className="search-container">
                <input
                    type="text"
                    placeholder="Search for a player..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Player</th>
                        <th onClick={() => handleSort('Passing Yards')} className={getSortClass('Passing Yards')}>Passing Yards</th>
                        <th onClick={() => handleSort('Passing TDs')} className={getSortClass('Passing TDs')}>Passing TDs</th>
                        <th onClick={() => handleSort('Interceptions')} className={getSortClass('Interceptions')}>Interceptions</th>
                        <th onClick={() => handleSort('Rushing Yards')} className={getSortClass('Rushing Yards')}>Rushing Yards</th>
                        <th onClick={() => handleSort('Rushing TDs')} className={getSortClass('Rushing TDs')}>Rushing TDs</th>
                        <th onClick={() => handleSort('Receptions')} className={getSortClass('Receptions')}>Receptions</th>
                        <th onClick={() => handleSort('Receiving Yards')} className={getSortClass('Receiving Yards')}>Receiving Yards</th>
                        <th onClick={() => handleSort('Receiving TDs')} className={getSortClass('Receiving TDs')}>Receiving TDs</th>
                        <th onClick={() => handleSort('Fumbles')} className={getSortClass('Fumbles')}>Fumbles</th>
                        {view === 'PPR' && <th onClick={() => handleSort('Fantasy PPR Points')} className={getSortClass('Fantasy PPR Points')}>Fantasy PPR Points</th>}
                        {view === 'Non-PPR' && <th onClick={() => handleSort('Fantasy Non-PPR Points')} className={getSortClass('Fantasy Non-PPR Points')}>Fantasy Non-PPR Points</th>}
                        <th>Add to Team</th>
                    </tr>
                </thead>
                <tbody>
                    {paginatedStats.map((stat, index) => (
                        <tr key={index}>
                            <td style={{ maxWidth: '200px', wordBreak: 'break-word' }}>{stat.Player}</td>
                            <td>{formatNumber(stat['Passing Yards'])}</td>
                            <td>{formatNumber(stat['Passing TDs'])}</td>
                            <td>{formatNumber(stat['Interceptions'])}</td>
                            <td>{formatNumber(stat['Rushing Yards'])}</td>
                            <td>{formatNumber(stat['Rushing TDs'])}</td>
                            <td>{formatNumber(stat['Receptions'])}</td>
                            <td>{formatNumber(stat['Receiving Yards'])}</td>
                            <td>{formatNumber(stat['Receiving TDs'])}</td>
                            <td>{formatNumber(stat['Fumbles'])}</td>
                            {view === 'PPR' && <td>{formatNumber(stat['Fantasy PPR Points'])}</td>}
                            {view === 'Non-PPR' && <td>{formatNumber(stat['Fantasy Non-PPR Points'])}</td>}
                            <td>
                                <button
                                    onClick={() => handleSelectPlayer(stat.Player)}
                                    className={selectedPlayers.includes(stat.Player) ? 'button-remove' : 'button-add'}
                                >
                                    {selectedPlayers.includes(stat.Player) ? 'Remove' : 'Add'}
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="pagination">
                <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
                    Next
                </button>
            </div>
            <div className="team-summary">
                <h2>Selected Players</h2>
                <ul>
                    {selectedPlayers.map((player, index) => (
                        <li key={index}>{player}</li>
                    ))}
                </ul>
                <p>Total Projected Points: {formatNumber(totalPoints)}</p>
                <button className="button-reset" onClick={handleResetTeam}>
                    Reset Team
                </button>
            </div>
        </div>
    );
};

export default PlayerStats;
