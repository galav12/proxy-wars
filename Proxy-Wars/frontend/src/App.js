import React ,{ useState, useEffect, act } from "react";
import {Button} from '@mui/material';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import './App.css';
import logo from './resources/logo.png'

const TableCorr = ({results}) =>{
    const sensitive = Object.keys(results.pearson);
    const columns = Object.keys(results.pearson[sensitive[0]]);

    return (
        <table className="Table" border="1">
            <thead>
                <tr>
                    <th></th>
                    {sensitive.map(sen => (
                        <th key={sen}>{sen}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {columns.map(col => (
                    <tr>
                        <th>{col}</th>
                        {sensitive.map(sen => (
                            <td style={{backgroundColor: getColorForValue(Math.abs((results.pearson[sen][col]+results.kendall[sen][col]+results.spearman[sen][col])/3), 1)}}>
                            Pearson: {results.pearson[sen][col]}<br/>
                            Kendall: {results.kendall[sen][col]}<br/>
                            Spearman: {results.spearman[sen][col]}<br/>
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

const getColorForValue = (value, maxValue) => {
    if (value === "NaN" || value === null) return "rgb(140,140,140)"; // White for NaN or null values
    const intensity = (parseFloat(value) / maxValue);
    return `rgba(${0}, ${0}, 255, ${intensity})`;
};


const TableFacet = ({results}) =>{
    const sensitive = Object.keys(results);
    const columns = Object.keys(results[sensitive[0]]);

    // Find the max value for scaling the heatmap colors
    const maxValue = 100;

    const getColorForValue = (value, maxValue) => {
        if (value === "NaN" || value === null) return "rgb(140,140,140)"; // White for NaN or null values
        const intensity = (parseFloat(value) / maxValue);
        return `rgba(${0}, ${0}, 255, ${intensity})`;
    };

    return (
        <div>
            <div style={{ display: "grid", gridTemplateColumns: `repeat(${sensitive.length + 1}, auto)`, gap: "4px" }}>
                {/* Header row */}
                <div></div>
                {sensitive.map((sen) => (
                    <div key={sen} style={{ fontWeight: "bold", textAlign: "center" }}>{sen}</div>
                ))}

                {/* Heatmap cells */}
                {columns.map((col) => (
                    <React.Fragment key={col}>
                        <div style={{ fontWeight: "bold", textAlign:"right" }}>{col}</div>
                        {sensitive.map((sen) => {
                            var value = results[sen][col];
                            if (value != "NaN") {
                            value = Math.round(results[sen][col] * 100) / 100;
                            }
                            return (
                                <div
                                    key={`${sen}-${col}`}
                                    style={{
                                        backgroundColor: getColorForValue(value, maxValue),
                                        padding: "10px",
                                        textAlign: "center"
                                    }}
                                >
                                    {value !== "NaN" ? `${value}%` : "NaN"}
                                </div>
                            );
                        })}
                    </React.Fragment>
                ))}
            </div>
            
            {/* Color Gradient Legend */}
            <div style={{
                display: 'grid', 
                alignItems: 'center', 
                justifyContent: 'center', 
                marginTop: '20px',
                height: '80px',
                width: '100%'
            }}>
                <div style={{ 
                    width: '500px', 
                    height: '40px', 
                    border: '2px solid gray',
                    background: 'linear-gradient(to right, rgba(0,0,255,0), rgba(0,0,255,1))',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '0 5px'
                }}>
                    
                </div>
                <div style={{ 
                    width: '500px', 
                    height: '40px', 
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '0 5px'
                }}>
                    <span>0%</span>
                    <span>100%</span>
                </div>
            </div>
        </div>
    );
};


const TableRules = ({rules}) =>{
    const rulesList = Object.keys(rules);

    return (
        <table className="RulesTable" border="1">
            <thead>
                <tr>
                    <th></th>
                    <th>Antecedents<InfoBoxButton text={"List of attributes that are input to the Rule. Includes min and max values of attributes.\n\nThe X part of \"If X, then Y\""}/></th>
                    <th>Consequents<InfoBoxButton text={"List of attributes that are output of the Rule. Includes min and max values of attributes.\n\nThe Y part of \"If X, then Y\""}/></th>
                    <th>Support<InfoBoxButton text={"Measures proportion of transactions that contain the attribute X.\n\nHigher support suggests that the variable is more significant for discovering associations"}/></th>
                    <th>Confidence<InfoBoxButton text={"Measures proportion of transactions that contain the target in the set of transactions that contain the itemset\n\nReflects the strength of the association"}/></th>
                    <th>Lift<InfoBoxButton text={"Measures how many times more often the itemset and target occur than if they were independent. It measures the strength of the association.\n\nA value greater than 1 indicates a strong positive association."}/></th>
                    {/* <th>Fitness</th> */}
                </tr>
            </thead>
        <tbody>
            {rulesList.map(col => (
                <tr>
                    <th key={col}>{Number(col) + 1}</th>
                    <td style={{width: "300px"}}>{rules[col]["antecedent"].join(", ")}</td>
                    <td style={{width: "300px"}}>{rules[col]["consequent"].join(", ")}</td>
                    <td style={{width: "150px"}}>{rules[col]["support"]}</td>
                    <td style={{width: "150px"}}>{rules[col]["confidence"]}</td>
                    <td style={{width: "150px"}}>{rules[col]["lift"]}</td>
                </tr>
            ))}
        </tbody>
        </table>
    );
};

const InfoBoxButton = ({ text }) => {
    return (
        <div className="InfoButton" style={{ position: 'relative', display: 'inline-block', marginLeft: '10px'}}>
            <button style={{ background: 'transparent', padding: '0', margin: '0', border: 'none', verticalAlign: 'middle'}}>
            <img src={require('./resources/info.svg').default}
                style={{ width: '20px', height: '20px'}} />
            </button>
            {(
                <div className="Info" style={{
                    position: 'absolute',
                    background: '#dae7f0',
                    padding: '10px',
                    minWidth: '250px',
                    maxWidth: '500px',
                    transform: 'translateX(-50%)',
                    fontWeight: 'normal',
                    color: '#000000',
                    borderRadius: '20px',
                    whiteSpace: 'pre-wrap',
                    zIndex: 1,
                }}>
                    {text}
                </div>
            )}
        </div>
    );
};

function App() {
    const [columns, setColumns] = useState([]);
    const [currColumns, setCurrColumns] = useState([]);
    let algorithms = ['Correlational Analysis','FACET','Association Rule Mining'];
    const [selectedAlgorithm, setSelectedAlgorithm] = useState("");
    const [selectedVariables, setSelectedVariables] = useState([]);
    const [limitingRows, setLimitingRows] = useState("");
    const [infoText, setInfoText] = useState('');
    const [sampleSize, setSampleSize] = useState("");
    const [seed, setSeed] = useState("-1");
    const [rowFilter, setRowFilter] = useState("");
    const [selectAll, setSelectAll] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const [file, setFile] = useState(null);
    const [displayResults, setDisplayResults] = useState(false);
    const [results, setResults] = useState(null);
    const [status, setStatus] = useState("");
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [sortCol, setSortCol] = useState(null)
    const [sortCoeff, setSortCoeff] = useState(null)
    const [targetVar, setTargetVar] = useState(null)
    const [startTime, setStartTime] = useState(null)
    const [endTime, setEndTime] = useState(null)
    const [currAlgorithm, setCurrAlgorithm] = useState(null);
    const [currentTime, setCurrentTime] = useState(Date.now());
    const [currFilter, setCurrFilter] = useState(null);
    const [currFile, setCurrFile] = useState(null);
    const [activeTab, setActiveTab] = useState('algorithm');
    const [resultsTab, setResultsTab] = useState('selected');
    const [ruleQuery, setRuleQuery] = useState(["",""]);
    const [ruleVars, setRuleVars] = useState([[],[]])
    const [selectedRules, setSelectedRules] = useState(null)
    const [filteredRules, setFilteredRules] = useState(null)
    const [filteredSelectedRules, setFilteredSelectedRules] = useState(null)
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [armSearchAnd, setArmSearchAnd] = useState(true);

    const algorithmInfo = {
        "Correlational Analysis": "Identifies the strength and direction of relationships between variables.",
        "FACET": "Finds relationships between variables using a feature selection approach.",
        "Association Rule Mining": "Calculates relationships between variables by generating association rules.",
    };

    const filteredVariables = currColumns.filter(variable => variable.toLowerCase().includes(searchQuery.toLowerCase()));
    
    function FilterRules(ruleVars) {
        if(armSearchAnd){
            setFilteredRules(results.filter(variable => {
                return (ruleVars[0].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["antecedent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        // console.log('Item:', item);
                        // console.log('Rule:', rule);
                        // console.log('Attribute Match:', attributeMatch);
                        // console.log('Min Range Valid:', minValid);
                        // console.log('Max Range Valid:', maxValid);
                        // console.log("");
                        return attributeMatch && minValid && maxValid;
                    });
                }) && ruleVars[1].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["consequent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }))
            }));
        }
        else {
            setFilteredRules(results.filter(variable => {
                return (ruleVars[0].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["antecedent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }) || ruleVars[1].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["consequent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }))
            }));
        }
    }

    function FilterSelectedRules(ruleVars) {
        if(armSearchAnd){
            setFilteredSelectedRules(selectedRules.filter(variable => {
                return (ruleVars[0].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["antecedent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }) && ruleVars[1].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["consequent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }))
            }));
        }
        else {
            setFilteredSelectedRules(selectedRules.filter(variable => {
                return (ruleVars[0].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["antecedent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }) || ruleVars[1].every(ruleStr => {
                    const rule = parseRule(ruleStr);
                    return variable["consequent"].some(itemStr => {
                        const item = parseItem(itemStr);
                        const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                        const minValid = rule.min <= item.min;
                        const maxValid = rule.max >= item.max;
                        return attributeMatch && minValid && maxValid;
                    });
                }))
            }));
        }
    }
    
    function FilterInitRules(results) {
        setSelectedRules(results.filter(variable => {
            return (selectedVariables.some(ruleStr => {
                const rule = parseRule(ruleStr);
                return variable["antecedent"].some(itemStr => {
                    const item = parseItem(itemStr);
                    const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                    const minValid = rule.min <= item.min;
                    const maxValid = rule.max >= item.max;
                    return attributeMatch && minValid && maxValid;
                });
            }) || selectedVariables.some(ruleStr => {
                const rule = parseRule(ruleStr);
                return variable["consequent"].some(itemStr => {
                    const item = parseItem(itemStr);
                    const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                    const minValid = rule.min <= item.min;
                    const maxValid = rule.max >= item.max;
                    return attributeMatch && minValid && maxValid;
                });
            }))
        }));
        setFilteredSelectedRules(results.filter(variable => {
            return (selectedVariables.some(ruleStr => {
                const rule = parseRule(ruleStr);
                return variable["antecedent"].some(itemStr => {
                    const item = parseItem(itemStr);
                    const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                    const minValid = rule.min <= item.min;
                    const maxValid = rule.max >= item.max;
                    return attributeMatch && minValid && maxValid;
                });
            }) || selectedVariables.some(ruleStr => {
                const rule = parseRule(ruleStr);
                return variable["consequent"].some(itemStr => {
                    const item = parseItem(itemStr);
                    const attributeMatch = item.attribute.toLowerCase().startsWith(rule.attribute.toLowerCase());
                    const minValid = rule.min <= item.min;
                    const maxValid = rule.max >= item.max;
                    return attributeMatch && minValid && maxValid;
                });
            }))
        }));
    }
    function parseRule(item) {
        if(item.includes('(')){
            const [attribute, range] = item.slice(0,-1).split('(');
            if(range.includes('-')){
                const [min, max] = range.split('-').map(val => val.trim());
                return {
                    attribute: attribute.toLowerCase(),
                    min: min === '*' ? -Infinity : Number(min),
                    max: max === '*' ? Infinity : Number(max)
                }
            }
            else {
                return {
                    attribute: attribute,
                    min: Number(range),
                    max: Infinity
                }
            }
        }
        else {
            return {
                attribute: item.toLowerCase().trim(),
                min: -Infinity,
                max: Infinity
            }
        }
    }
    function parseItem(item) {
        const [attribute, range] = item.slice(0,-1).split('(');
        const [min, max] = range.split(',').map(val => val.trim());
        return {
            attribute: attribute.toLowerCase(),
            min: min === '*' ? -Infinity : Number(min),
            max: max === '*' ? Infinity : Number(max)
        }
    }
    const handleAlgorithm = (event) => {
        setSelectedAlgorithm(event.target.value);
        if(event.target.value === "Correlational Analysis"){
            setTargetVar(null);
            setCurrColumns(columns);
        }
        setInfoText(algorithmInfo[event.target.value] || '');
        console.log(event.target.value);
    };
    const handleCheckboxChange = (variable) => {
        if (selectedVariables.includes(variable)) {
            setSelectedVariables(selectedVariables.filter(item => item !== variable));
        } else {
            setSelectedVariables([...selectedVariables, variable]);
        }
        console.log(selectedVariables);
    };
    const handleSelectAll = () => {
        console.log(selectAll);
        setSelectAll(!selectAll);
        if(selectAll){
            setSelectedVariables(selectedVariables.filter((item) => !filteredVariables.includes(item)));
        }
        else {
            setSelectedVariables([...new Set([...selectedVariables, ...filteredVariables])]);
        }
        console.log(selectedVariables);
    }
    const handleSearch = (event) => {
        setSearchQuery(event.target.value);
        setSelectAll(false);
    }
    const handleFile =(event) => {
        const currFile = event.target.files[0];
        if(!currFile || !currFile.name.endsWith('.csv')){
            alert("Please upload a .csv file with dataset to analyze");
        }
        else if (event.target.files[0].size > 3 * 1000 * 1000 * 1024) {
            alert("File with maximum size of 3 GB is allowed")
        }
        else {
            setFile(event.target.files[0]);
        }
        console.log("File Selected");
    }
    const handleLimitingRows = (event) => {
        setLimitingRows(event.target.value);
        console.log(event.target.value);
    };
    const handleSample = (event) => {
        if(event.target.value < 0 || event.target.value > 100){
            alert("Invalid Sample Size. Please enter value between 0 and 100.")
            return
        }
        setSampleSize(event.target.value);
        console.log(event.target.value);
    };
    const handleSeed = (event) => {
        if(event.target.value < 0){
            alert("Invalid Seed. Seed must be a non-negative integer");
            return;
        }
        setSeed(event.target.value);
        console.log(event.target.value);
    };
    const handleRowFilter = (event) => {
        setRowFilter(event.target.value);
        console.log(event.target.value);
    };
    const handleSortCol = (event) => {
        setSortCol(event.target.value);
        console.log(event.target.value);
    }
    const handleSortCoeff = (event) => {
        setSortCoeff(event.target.value);
        console.log(event.target.value);
    }
    const handleTargetVar = (event) => {
        setTargetVar(event.target.value);
        setSelectedVariables(selectedVariables.filter(item => item !== event.target.value));
        setCurrColumns(columns.filter(item => item !== event.target.value));
        console.log(event.target.value);
    }
    const handleRuleSearchAntecedent = (event) => {
        setRuleQuery([event.target.value, ruleQuery[1]]);
        setRuleVars([event.target.value.split(',').map(val => val.trim()), ruleVars[1]]);
        console.log(ruleQuery)
        console.log(ruleVars)
    }
    const handleRuleSearchConsequent = (event) => {
        setRuleQuery([ruleQuery[0],event.target.value]);
        setRuleVars([ruleVars[0], event.target.value.split(',').map(val => val.trim())]);
        console.log(ruleQuery)
        console.log(ruleVars)
    }
    const handleRuleSearchButton = () => {
        FilterRules(ruleVars);
        FilterSelectedRules(ruleVars);
    }
    const handleClearFilterButton = () => {
        setRuleQuery(["",""]);
        setRuleVars([[],[]]);
        FilterRules([[],[]]);
        FilterSelectedRules([[],[]]);
    }
    const handleArmSearchAnd = (event) => {
        setArmSearchAnd(!armSearchAnd);
    };
    useEffect(() => {
        if (loading) {
          const interval = setInterval(() => {
            setCurrentTime(Date.now());
          }, 50);
          return () => clearInterval(interval);
        } else {
          setCurrentTime(Date.now());
        }
    }, [loading]);
    
      useEffect(() => {
        if (uploading) {
          const interval = setInterval(() => {
            setCurrentTime(Date.now());
          }, 50);
          return () => clearInterval(interval);
        } else {
          setCurrentTime(Date.now());
        }
    }, [uploading]);

    const handleUpload = async () => {
        if(!file || !file.name.endsWith('.csv')){
            alert("No file selected");
            return;
        }
        setStartTime(Date.now());
        setUploading(true);
        const data = new FormData();
        data.append('file', file);

        const uploadResponse = await fetch('/api/upload',{
            method: 'POST',
            body: data,
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => alert(error));
        // .catch(error => console.log('Error: ', error));

        console.log("File uploaded")
        setColumns([]);
        setSelectedVariables([]);
        setSelectAll(false);
        setTargetVar(null);
        setCurrFile(file);

        const getResponse = await fetch('/api/columns')
        .then(response => response.json())
        .then(data => {
            setColumns(data.columns);
            setCurrColumns(data.columns);
        })
        .catch(error => alert(error));
        // .catch(error => console.log('Error: ', error));
        setUploading(false);
    }

    const handleResults = async () => {
        
        setStartTime(Date.now());

        setLoading(true);
        setDisplayResults(false);

        setCurrAlgorithm(selectedAlgorithm);
        console.log(currAlgorithm);

        const algResponse = await fetch('/api/algorithm',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({algorithm: selectedAlgorithm}),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => alert(error));
        // .catch(error => console.log('Error: ', error));

        if(selectedAlgorithm === "FACET" || selectedAlgorithm === "Association Rule Mining"){
            const targetResponse = await fetch('/api/target-variable',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({target: targetVar}),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => alert(error));
            // .catch(error => console.log('Error: ', error));
        }

        if(limitingRows === "complete"){
            const rowResponse = await fetch('/api/random', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    percentage: "100",
                    seed: seed,
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => alert(error));
            // .catch(error => console.log('Error: ', error));
        }
        else if(limitingRows === "random"){
            console.log("RANDOM")
            const rowResponse = await fetch('/api/random', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    percentage: sampleSize,
                    seed: seed,
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => alert(error));
            // .catch(error => console.log('Error: ', error));
        }
        else if (limitingRows === "filter") {
            console.log("FILTER")
            setCurrFilter(rowFilter);
            const rowResponse = await fetch('/api/filter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: rowFilter,
                    seed: seed,
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => alert(error));
            // .catch(error => console.log('Error: ', error));
        }
        
        const varResponse = await fetch('/api/sensitive-variables',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({variables: selectedVariables}),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => alert(error));
        // .catch(error => console.log('Error: ', error));

        const resultResponse = await fetch('/api/results', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (resultResponse.ok) {
            const data = await resultResponse.json();
            setStatus(data.status);

            if (data.results) {
                if(selectedAlgorithm === "Correlational Analysis"){
                    let col = sortCol === null ? selectedVariables[0] : sortCol;
                    let coeff = sortCoeff === null ? "pearson" : sortCoeff;
                    const sortedResults = sortCorr(data.results, col, coeff);
                    setResults(sortedResults);
                }
                else if(selectedAlgorithm === "Association Rule Mining") {
                    setResults(data.results);
                    setFilteredRules(data.results);
                    setFilteredSelectedRules(data.results);
                    FilterInitRules(data.results);
                }
                else {
                    setResults(data.results);
                }
                
            } else {
                setResults(null);
            }

        } else {
            const error = await resultResponse.text();
            alert(error);
            // console.log('Error:', error);
        }

        setLoading(false);
        setDisplayResults(true);
        setActiveTab('results');
        setEndTime(Date.now());
    }

    const sortCorr = (results, sensitiveVariable, method) => {
        if (!results || !results[method] || !results[method][sensitiveVariable]) {
            console.log("Error: could not find results or variables");
            return {};
        }
      
        const sensitiveCorrelations = results[method][sensitiveVariable];
        const sortedColumns = Object.keys(sensitiveCorrelations).sort((a, b) => Math.abs(sensitiveCorrelations[b]) - Math.abs(sensitiveCorrelations[a]));
        const sortedResults = {};
        
        for (const m in results) {
            sortedResults[m] = {};
            sortedColumns.forEach(sv => {
                if (results[m][sv]) {
                    sortedResults[m][sv] = {};
                    sortedColumns.forEach(col => {
                        sortedResults[m][sv][col] = results[m][sv][col];
                    });
                }
            });
        }
        setResults(sortedResults);
        return sortedResults;
    };

    const sortFacet = (results, sensitiveVariable) => {
        if (!results || !results[sensitiveVariable] || sensitiveVariable === targetVar) {
            console.log("Error: coudl not find results or variables");
            return {results};
        }

        const sensitiveCorrelations = results[sensitiveVariable];
        const sortedColumns = Object.keys(sensitiveCorrelations).sort((a, b) => {
            let a_val = sensitiveCorrelations[a];
            let b_val = sensitiveCorrelations[b];
            if(a_val === "NaN" && b_val !== "NaN"){
                return -1;
            }
            if(a_val !== "NaN" && b_val === "NaN"){
                return 1;
            }
            return Math.abs(b_val) - Math.abs(a_val)
        });
        const sortedResults = {};
        
        sortedColumns.forEach(sv => {
            if (results[sv]) {
                sortedResults[sv] = {};
                sortedColumns.forEach(col => {
                    sortedResults[sv][col] = results[sv][col];
                });
            }
        });
        setResults(sortedResults);
        return sortedResults;
    }

  return (
    <div className={`App ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
        <div className="Wrapper-Header">
            <div style={{width: '10%'}} />
            <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '80%' }}>
                {/* <h1 style = {{color: '#0766D1'}} className='Title'>Proxy Wars </h1> */}
                <img src={logo} width={'230px'} alt="Logo" />
                <h1 style = {{marginLeft: '10px'}} className='Title'>- A Proxy Variable Exploration Tool</h1>
            </header>
            <div style={{display: 'flex', justifyContent: 'center', width: '10%', verticalAlign: 'middle', height: '75px', paddingTop: '15px', paddingRight: '15px'}}>
            <Button variant="text" style={{width: '80px', height: '50px', borderRadius: '20px'}} sx={{border: '2px solid #0766D1', '&:hover': {backgroundColor: !isDarkMode ? '#2f2f2f' : '#ffffff', color: !isDarkMode ? '#ffffff' : "#0766D1"}}}
                onClick={() => setIsDarkMode(!isDarkMode)}>
                {isDarkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </Button>
            </div>
        </div>
        <div className="tabs">
            <button onClick={() => setActiveTab('algorithm')} className={activeTab === 'algorithm' ? 'tab-active' : 'tab'}>
                Algorithm
            </button>
            <button onClick={() => setActiveTab('results')} className={activeTab === 'results' ? 'tab-active' : 'tab'}>
                Results
            </button>
        </div>

        {activeTab === 'algorithm' && (
            <>
                <div className="Wrapper">
                    <div className="Details">
                        {/* Upload DataSet */}
                        <div className="Upload">
                            <br /><font color="#0766D1"><u><b style={{fontSize: '16px', color: isDarkMode ? '#ffffff' : '#0766D1'}}>Upload Dataset:</b></u></font>{<InfoBoxButton text={"Upload a CSV file containing the dataset. \n\nOnly Numerical Fields will be analyzed"} />}
                            <br/>
                            <input type="file" onChange={handleFile} style={{ fontSize: '16px', padding: '8px 12px', borderRadius: '10px', marginTop: '10px' }}/>
                            <button className="Upload" type="button" onClick={handleUpload}
                            >Upload</button>
                            <br/>
                            {uploading ? <div>Uploading: {(currentTime - startTime)/1000.0} Seconds<br/></div> : null}
                            {!uploading && currFile && "Upload successful - " + currFile.name}
                        </div>

                        {/* Select Algorithm */}
                        <div style={{marginTop: '15px', marginBottom: '10px'}}><font color="#0766D1"><u><b style={{fontSize: '16px', color: isDarkMode ? '#ffffff' : '#0766D1'}}>Select Algorithm:</b></u></font>&emsp;
                            <select onChange={handleAlgorithm} value={selectedAlgorithm}>
                                <option value="" hidden>Select an Algorithm</option>
                                {algorithms.map((item, index) => (
                                    <option key={index} value={item}>{item}</option>
                                ))}
                            </select>
                            {selectedAlgorithm && <InfoBoxButton text={infoText} />}
                            <br/>
                            {/* Select Target Variable for FACET */}
                            {selectedAlgorithm !== "FACET" ? null : " "} {selectedAlgorithm !== "FACET" ? null :
                                <div>
                                    <font color="#0766D1"><u><b style={{fontSize: '16px', color: isDarkMode ? '#ffffff' : '#0766D1'}}>Target Variable:</b></u></font>&emsp;
                                    <select onChange={handleTargetVar} value={targetVar}>
                                        <option value="" hidden>Select a Target Variable</option>
                                        {columns.map((item, index) => (
                                            <option key={index} value={item}>{item}</option>
                                        ))}
                                    </select>
                                    <InfoBoxButton text={"Select the variable to train the FACET model on"} />
                                    <br/>
                                </div>
                            }
                            {/* Select Random seed for FACET and dataset limiting */}
                            <font color="#0766D1"><u><b style={{fontSize: '16px', color: isDarkMode ? '#ffffff' : '#0766D1'}}>Random Seed:</b></u></font>&emsp;<input type="number" onChange={handleSeed} style={{width: '50px', height: '20px'}} min={0} />
                            <br/>
                            <div style={{ marginTop: '20px', marginBottom: '10px' }}><font color="#0766D1"><u><b style={{fontSize: '16px', color: isDarkMode ? '#ffffff' : '#0766D1'}}>Limit Dataset: </b></u></font></div>
                            <input type="radio" value="complete" checked={limitingRows === "complete"} onChange={handleLimitingRows} style={{marginTop: '5px', marginBottom: '20px'}} />Complete Dataset <br />
                            <input type="radio" value="random" checked={limitingRows === "random"} onChange={handleLimitingRows} />Simple Random Sample: <input type="number" onChange={handleSample} disabled={limitingRows !== "random"} max="100" min="0" style={{width: '50px', height: '20px', marginBottom: '10px'}} value={sampleSize} /> % &emsp;
                            <br/>
                            <input type="radio" value="filter" checked={limitingRows === "filter"} onChange={handleLimitingRows} />SQL WHERE Filter: <input type="text" onChange={handleRowFilter} disabled={limitingRows !== "filter"} value={rowFilter} style={{width: '185px', height: '25px', marginBottom: '10px'}} />
                            <InfoBoxButton text={"Use SQL WHERE syntax for filtering rows. \n\nExample: \" age > 30 and age < 50 \" "} />
                        </div>
                    </div>

                    <div className="Columns">
                        {/* <div className={selectedAlgorithm === "Association Rule Mining" ? "Columns-sensitive-disabled" : "Columns-sensitive"}> */}
                        <div className={"Columns-sensitive"}>
                            <h3>{selectedAlgorithm === "Association Rule Mining" ? "Selected Variables:" : "Sensitive Variables:"}</h3>
                            {columns.length === 0 ? (
                                <div>No Variables Available</div>
                            ) : (
                                <div>
                                    <input className="checkbox-variables" type="text" placeholder="Search Variables" onChange={handleSearch} /><br/>
                                    <input className="checkbox-variables" type="checkbox" checked={filteredVariables.every(filteredVar => selectedVariables.includes(filteredVar))} onChange={handleSelectAll} />Select All
                                    {filteredVariables.map((item, idx) =>(
                                        <div key={idx}>
                                            <input className="checkbox-variables" type="checkbox" checked={selectedVariables.includes(item)} onChange={() => handleCheckboxChange(item)} />{item}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                <div className="Results">
                    <button type="button" disabled={!file || selectedAlgorithm === "" || limitingRows === ""} onClick={handleResults}>Results</button>
                </div>
                <div className="Results-div">{loading ? <div>Loading
                : {(currentTime - startTime)/1000.0} Seconds<br/></div> : null}
                </div>
            </>
        )}
        {activeTab === 'results' && (
            <>
                <div className="Sort" hidden={!displayResults || !results}  >
                    <div hidden={currAlgorithm === "Association Rule Mining"}><font color="#0766D1"><u><b style={{fontSize: '16px'}}>Sort Table:</b></u></font></div>
                    <div className="Corr-sort" hidden={!displayResults || !results || selectedAlgorithm !== "Correlational Analysis"}>
                        Select Column to be sorted on:&emsp;
                        <select onChange={handleSortCol} value={sortCol}>
                            <option value="" hidden>Select a Column</option>
                            {selectedVariables.map((item, index) => (
                                <option key={index} value={item}>{item}</option>
                            ))}
                        </select><br/>
                        Select Coefficient to be sorted on:&emsp;
                        <select onChange={handleSortCoeff} value={sortCoeff}>
                            <option value="" hidden>Select a Coefficient</option>
                            <option key="0" value="pearson">Pearson</option>
                            <option key="1" value="kendall">Kendall</option>
                            <option key="2" value="spearman">Spearman</option>
                        </select><br/>
                        <button type="button" hidden={!results} onClick={() => {
                            let col = sortCol === null || sortCol === "" ? selectedVariables[0] : sortCol;
                            let coeff = sortCoeff === null || sortCol === "" ? "pearson" : sortCoeff;
                            const sortedResults = sortCorr(results, col, coeff);
                            setResults(sortedResults);
                        }}>Sort</button>
                    </div>
                    <div className="Facet-sort" hidden={!displayResults || !results || selectedAlgorithm !== "FACET"}>
                        <br/>
                        Select Column to be sorted on:&emsp;
                        <select onChange={handleSortCol} value={sortCol}>
                            <option value="" hidden>Select a Column</option>
                            {selectedVariables.filter(item => item !== targetVar).map((item, index) => (
                                <option key={index} value={item}>{item}</option>
                            ))}
                        </select><br/>
                        <button type="button" hidden={!results} onClick={() => {
                            let col = sortCol === null || "" ? selectedVariables[0] : sortCol;
                            const sortedResults = sortFacet(results, col);
                            setResults(sortedResults);
                        }}>Sort</button>
                    </div>
                </div>
                <div className="Results-div" style={{ visibility: displayResults ? 'visible' : 'hidden' }}>
                    <div style={{fontWeight: 'bold'}}>{status}</div>
                    <div><span style={{color: '#0766D1'}}>Algorithm Time:</span> {(endTime - startTime)/1000.0} Seconds</div>
                    <div><span style={{color: '#0766D1'}}>{selectedAlgorithm === "Association Rule Mining" ? "Selected Variables:" : "Sensitive Variables:"}</span> {selectedVariables.join(", ")}</div>
                    <div><span style={{color: '#0766D1'}}>Random Seed:</span> {seed === "-1" ? "No Seed Selected" : seed}</div>
                    <div hidden={limitingRows !== "random" || !sampleSize}><span style={{color: '#0766D1'}}>Random Sample:</span> {sampleSize}%</div>
                    <div hidden={limitingRows !== "filter" || !rowFilter}><span style={{color: '#0766D1'}}>SQL Filter:</span> WHERE {currFilter}</div>
                    <br/>
                    <div>Results:<br/><br/></div>
                    {/* {JSON.stringify(results, null, 2)} */}
                    {displayResults && results && currAlgorithm === "Correlational Analysis" && <TableCorr results={results} />}
                    {displayResults && results && currAlgorithm === "FACET" && <TableFacet results={results} />}
                    {displayResults && results && currAlgorithm === "Association Rule Mining" && (
                        <>
                            <div className="tabs">
                                <button onClick={() => setResultsTab('all')} className={resultsTab === 'all' ? 'tab-results-all-active' : 'tab-results-all'}>All Rules</button>
                                <button onClick={() => setResultsTab('selected')} className={resultsTab === 'selected' ? 'tab-results-selected-active' : 'tab-results-selected'}>Rules for Selected Variables</button>
                            </div>
                            <br/>
                            <div className="SearchRules">
                                Antecedent: &emsp;<input type="text" placeholder="Search Rules" onChange={handleRuleSearchAntecedent} value={ruleQuery[0]} />&emsp;<input type="radio" checked={armSearchAnd === true} onChange={handleArmSearchAnd}/>And<input type="radio" checked={armSearchAnd === false} onChange={handleArmSearchAnd}/>Or
                                <br/>
                                Consequent:&emsp;<input type="text" placeholder="Search Rules" onChange={handleRuleSearchConsequent} value={ruleQuery[1]} />&emsp;
                                <InfoBoxButton text={"Search for variables by selecting an option and entering a comma-separated list of variables. To specify a range, simply include the minimum and maximum values in parentheses next to the variable.\n\nFor example, \"age(15-*), pclass(*-3), embarked(0-1), sibsp\" in Antecedent and \"survived(1)\" in Consequent"} /><br/>
                                <div style={{marginLeft: "175px"}}><button className="Rules" onClick={handleRuleSearchButton}>Apply Filter</button>&emsp;<button className="Rules" onClick={handleClearFilterButton}>Clear Filter</button><br/><br/></div>
                                {resultsTab === "all" && displayResults && results && currAlgorithm === "Association Rule Mining" && <TableRules rules={filteredRules} /> }
                                {resultsTab === "selected" && displayResults && results && currAlgorithm === "Association Rule Mining" && <TableRules rules={filteredSelectedRules} /> }
                            </div>
                        </>
                    )}
                </div>
            </>
        )}
    </div>
  );
}

export default App;
