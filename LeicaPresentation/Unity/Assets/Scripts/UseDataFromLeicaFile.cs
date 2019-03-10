using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class UseDataFromLeicaFile : MonoBehaviour
{
	[SerializeField]
	private string jsonStringData;
	[SerializeField]
	private string _nameFileLeica = "data.json";
	[SerializeField]
	private DataOneMeasureLeicaAll datas;

	private const double HEIGHT = 1.46;
	
	[SerializeField]
	private GameObject prefabPointCoordinate;

	private void Awake()
	{
		jsonStringData = File.ReadAllText(Application.dataPath + "/Ressources/" + _nameFileLeica);
		
		datas = JsonUtility.FromJson<DataOneMeasureLeicaAll>(jsonStringData);
		
	}

	private void Start()
	{
		foreach (DataOneMeasureLeica dataFromMeasure in datas.datas)
		{
			if (dataFromMeasure.RC.Equals("0:1285")) continue;
			GameObject gameObject = Instantiate(prefabPointCoordinate);
			gameObject.name = dataFromMeasure.lengthSlope + ";" +
							dataFromMeasure.angleHorizontal + ";" + dataFromMeasure.angleVertical;
			gameObject.transform.position = convertSphereCoordinateInToCartesianCoordinates(float.Parse(dataFromMeasure.lengthSlope, CultureInfo.InvariantCulture.NumberFormat),
				float.Parse(dataFromMeasure.angleHorizontal, CultureInfo.InvariantCulture.NumberFormat),
				float.Parse(dataFromMeasure.angleVertical, CultureInfo.InvariantCulture.NumberFormat));
		}
	}

	private Vector3 convertSphereCoordinateInToCartesianCoordinates(float r, float angleHorizontal, float angleVertical)
	{
		double x = r * Math.Sin(angleVertical) * Math.Cos(angleHorizontal);
		double y = r * Math.Sin(angleVertical) * Math.Sin(angleHorizontal);
		double z = r * Math.Cos(angleVertical) + HEIGHT;
		
		return new Vector3((float)x, (float)y, (float)z);
	}
}

[Serializable]
public class DataOneMeasureLeicaAll
{
	public List<DataOneMeasureLeica> datas;
}

[Serializable]
public class DataOneMeasureLeica
{
	public string R1P;
	public string angleHorizontal;
	public string value0;
	public string lengthSlope;
	public string RC;
	public string modeMeasure;
	public string angleVertical;
}
